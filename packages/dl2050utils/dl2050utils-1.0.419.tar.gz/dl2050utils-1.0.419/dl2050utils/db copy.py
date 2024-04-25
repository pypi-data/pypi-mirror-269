"""
    db.py
    DB Class

    ...

    json types are possible as inputs, just pass a python dict as field value

"""
import asyncio
import asyncpg
import datetime
import re
from pathlib import Path
import json
import orjson
import numpy as np
from dl2050utils.core import listify, oget, check_str, check_dict, check
from dl2050utils.log import BaseLog
from dl2050utils.fs import pickle_save, pickle_load

# TODO
#   SELECT
#       1) Lookup table id col name must be different than original table id col name due to SQL result cols name clash
#       2) nrows: returning 2 for results with one row, and 1 instead of zero when there are no results

# ####################################################################################################
# Helper functions
# ####################################################################################################

def strip(e):
    if type(e)!=str: return e
    e = e.replace('\'', '')
    e.replace('\"', '')
    e.replace('\n', ' ')
    return e

def get_repr(e):
    if e is None: return 'null'
    if type(e)==str: return f"'{strip(e)}'"
    if type(e) in [int,float]: return str(e)
    if type(e)==asyncpg.pgproto.pgproto.UUID: return f"'{e}'"
    if type(e)==datetime.datetime:
        s = e.strftime("%Y-%m-%d %H:%M:%S")
        return f"'{s}'"
    if type(e)==np.str_: return f"'{strip(str(e))}'"
    if np.issubdtype(type(e), np.str_): return f"'{strip(str(e))}'"
    if np.issubdtype(type(e), np.integer) or np.issubdtype(type(e), np.floating): return str(e)
    if type(e)==list:
        items = [f'"{str(e1)}"' for e1 in e]
        return f"'{{{' ,'.join(items)}}}'"
    if type(e)==dict:
        s = orjson.dumps(e, option=orjson.OPT_SERIALIZE_NUMPY).decode()
        return f"'{s}'"
    return str(e)

def get_select_q(tbl, join=None, filters=None, sfilters=None, cols='*', sort=None, ascending=True, offset=None, limit=None):
    # FIX: include offset,limit here - currently they are implemented in query()
    cols = '*' if cols is None else ', '.join(cols)
    offset,limit = offset or 0,limit or 32
    q = f"SELECT {cols} FROM {tbl}"
    join = parse_join(join)
    if join is not None:
        q += f" join {join['tbl2']} on {tbl}.{join['key1']}={join['tbl2']}.{join['key2']}"
        if not filters: filters = []
        filters.append({'col':f"{join['tbl2']}.{join['col']}", 'val':join['val']})
        # cols = [f'{tbl}.{e}' for e in cols]
    fs,sfs = parse_filters(filters),parse_filters(sfilters)
    fs = [{**e, 'op':'='} if 'op' not in e else e for e in fs]
    if len(fs):
        # TODO: include nulls -> <col> is null
        fs = ' AND '.join([f"{e['col']}{e['op']}{get_repr(e['val'])}" for e in fs])
        q += f" WHERE {fs}"
    if len(sfs):
        q+=' WHERE ' if not len(fs) else ' AND '
        q += ' AND '.join([f"{e['col']} ILIKE '%{e['val']}%'" for e in sfs])
    if isinstance(sort, str):
        q += f" ORDER BY {sort} " + ("ASC" if ascending else "DESC")
    q += ';'
    # Replace every '=null' by ' is null'
    q = re.sub(r'=null', ' is null', q, flags=re.IGNORECASE)
    return q

def fix_types(d):
    for k in d.keys():
        if isinstance(d[k], str):
            d[k] = d[k].strip()
        if isinstance(d[k], datetime.datetime):
            d[k] = d[k].strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(d[k], datetime.date):
            d[k] = d[k].strftime("%Y-%m-%d")
    return d

def parse_filters(fs):
    if fs is None or type(fs)!=dict and type(fs)!=list:
        return []
    if type(fs)==list:
        fs2 = []
        for e in fs:
            f = check_dict(e, keys=['col','val','op'])
            if f is not None and 'col' in f and 'val' in f:
                fs2.append(f)
        return fs2
    if type(fs)==dict:
        return [{'col':check_str(e, n=1024), 'val':check(fs[e])} for e in fs]
    return []

def parse_join(join):
    cols = ['tbl2', 'key1', 'key2', 'col', 'val']
    if type(join)!=dict: return None
    for e in cols:
        if e not in join: return None
    return {e:check(join[e]) for e in cols}

async def calc_query_rows(con, q):
    """
        Returns the exepected number of rows in a query.
        The number of rows is obtained by changing the query to count(*) and dropping the sort.
        TODO: Fix: the se explain fail on joins
    """
    # if 'join' in q:
    # q = q.lower()
    q1 = re.sub(r'SELECT .*? FROM', 'SELECT count(*) FROM', q, flags=re.IGNORECASE)
    q1 = re.sub(r'ORDER BY .*?$', '', q1, flags=re.IGNORECASE)
    res = await con.fetchrow(q1)
    if res is None: return None
    return dict(res)['count']
    # db.sync_select('pg_class', cols=['reltuples'], filters={'relname': 'diagsg'})
    res = await con.fetchrow(f'explain(format json) {q}')
    if res is None: return None
    res = json.loads(res['QUERY PLAN'])
    if res is None or not len(res): return None
    return oget(res[0],['Plan','Plan Rows'])

# ####################################################################################################
# DB Class
#
#   startup
#   shutdown
#
#   query
#   select
#   select_one
#   insert
#   update
#   update_or_insert
#   delete
#   get_seq
#
# ####################################################################################################

class DB():
    """
        Class for managing interactions with a PostgreSQL database.

        Constructor Parameters:
                - cfg (dict, optional): DB connection parameters (default: None, and a basic connection is provided).
                - log (BaseLog, optional): Logging mechanism for error and status messages (default: None).
                - dbname (str, optional): Name of the database to connect to (default: None).

            Methods:
                - async startup(min_size=5, max_size=20, loop=None)
                  Initiates the database connection pool with optional size and loop parameters.
                - shutdown()
                  Gracefully closes the database connection pool.
                - async execute(q)
                  Executes SQL queries (non-SELECT) and returns the result.
                - async def query(q, one=False, nrows=False, offset=None, limit=None)
                  Executes SELECT queries and retrieves data.
                - async get_trows(tbl) (Internal)
                  Retrieves the total number of rows that will result in a querty (through query planner).
                - async select(tbl, join=None, filters=None, sfilters=None, cols='*', sort=None, ascending=True, offset=None, limit=None, one=False)
                  Retrieves data from a table with filtering, sorting, and pagination options.
                - async select_one(tbl, filters=[])
                  Retrieves a single row from a table with optional filters.
                - async insert(tbl, d, return_key=None)
                  Inserts data into a table and optionally returns the inserted key.
                - async update(tbl, ks, d)
                  Updates rows in a table based on provided keys.
                - async update_or_insert(tbl, ks, d)
                  Updates rows if they exist, otherwise inserts new rows.
                - async delete(tbl, k, v)
                  Deletes rows from a table based on a key-value pair.
                - update_stats()
                  Performs a vacuum analyze operation for database statistics update (needed for query planner to work properly)

                The DB class assumes the use of a PostgreSQL database and proper configuration parameters for connection.
                Error messages and context information are logged for debugging purposes, enhancing reliability and maintainability.
                Ensures data integrity and security by validating and sanitizing input data.

                The filtering in define by two optional distint ways:
                    1) As an array of dict objects of the for {'col':col, 'val':val, 'op':op.} Op can be wither =,>,>=,<,<=,!=. 
                    2) Single dict with all the keys/vals.
    """
    def __init__(self, cfg=None, log=None, dbname=None, passwd=None):
        if cfg is None: cfg={'db':{'host':'db','port':5432,'user':'postgres','passwd':'rootroot','dbname':'postgres'}}
        self.cfg, self.LOG = cfg, log or BaseLog()
        host = oget(cfg,['db','host'],'db')
        port = oget(cfg,['db','port'],5432)
        user = oget(cfg,['db','user'],'postgres')
        passwd = oget(cfg,['db','passwd'],passwd)
        if dbname is None:
            dbname = oget(cfg,['db','dbname'],'postgres')
        self.url = f'postgres://{user}:{passwd}@{host}:{port}/{dbname}'
        self.dbname = dbname

    async def startup(self, min_size=5, max_size=20, loop=None):
        try:
            self.pool = await asyncpg.create_pool(self.url, min_size=min_size, max_size=max_size, loop=loop)
        except Exception as e:
            self.LOG(4, 0, label='DBPG', label2='STARTUP', msg=str(e))
            return True
        self.LOG(2, 0, label='DBPG', label2='STARTUP', msg=f'CONNECTED POOL to {self.dbname}')
        return False

    def shutdown(self):
        self.pool.terminate()
        self.LOG(2, 0, label='DBPG', label2='shutdown', msg='DISCONNECTED')
        return False
    
    async def execute(self, q):
        con = await self.pool.acquire()
        try:
            res = await con.execute(q)
        except Exception as err:
            self.LOG(4, 0, label='DBPG', label2='execute', msg={'error_msg': str(err), 'query': q})
            return None
        finally:
            await self.pool.release(con)
        return res

    async def query(self, q, one=False, nrows=False, offset=None, limit=None):
        con = await self.pool.acquire()
        if q[:6].upper()!='SELECT':
            one=True # accounts for returning in insert
        if one:
            nrows=False
        try:
            if(one):
                res = await con.fetchrow(q)
                if res is None:
                    await self.pool.release(con)
                    return None
            else:
                if nrows:
                    nr = await calc_query_rows(con, q)
                    if nr is None:
                        self.LOG(4, 0, label='DB', label2='calc_query_rows', msg=q)
                        await self.pool.release(con)
                        return None
                if offset or limit:
                    q=q[:-1]
                if offset is not None:
                    q += f" OFFSET {offset}"
                if limit is not None:
                    q += f" LIMIT {limit}"
                res = await con.fetch(q)
        except Exception as e:
            self.LOG(4, 0, label='DB', label2='query', msg=str(e))
            return None
        finally:
            await self.pool.release(con)
        if res is None:
            return None
        if(one):
            return fix_types(dict(res))
        # res = [fix_types(dict(row)) for row in res[:100000]]
        res = [fix_types(dict(row)) for row in res]
        if nrows:
            return {'data':res, 'nrows':nr}
        return res
    
    async def get_trows(self, tbl):
        q = f"select reltuples as nrows from pg_class where relname='{tbl}'"
        con = await self.pool.acquire()
        res = await con.fetchrow(q)
        if res is None:
            return -1
        return int(dict(res)['nrows'])

    async def select(self, tbl, join=None, filters=None, sfilters=None, cols='*', sort=None, ascending=True, offset=None, limit=None, one=False):
        q = get_select_q(tbl, join=join, filters=filters, sfilters=sfilters, cols=cols, sort=sort, ascending=ascending, offset=offset, limit=limit)
        return await self.query(q, one=one, nrows=True, offset=offset, limit=limit)

    async def select_one(self, tbl, filters=[]):
        return await self.select(tbl, filters=filters, one=True)
    
    async def insert(self, tbl, d, return_key=None):
        q = f"INSERT INTO {tbl} ("
        for k in d.keys(): q += f"{k}, "
        q = q[:-2] + ") VALUES ("
        for k in d.keys(): q = q + get_repr(d[k]) + ', '
        q = q[:-2] + ")"
        if return_key is not None:
            q += f" returning {return_key};"
            res = await self.query(q, one=True)
            if res is not None and len(res):
                return res[return_key]
            return None
        res = await self.execute(q)
        if res=='INSERT 0 1':
            return False
        return True

    async def update(self, tbl, ks, d):
        ks = listify(ks)
        for k in ks:
            if not k in d:
                self.LOG(4, 0, label='DBPG', label2='update', msg=f'key error: {k}')
                return True
        setvars = ', '.join([f"{k}={get_repr(d[k])}" for k in d if k not in ks+['nrows']])
        q = f"UPDATE {tbl} SET {setvars}"
        filters = ' AND '.join([f"{k}='{d[k]}'" for k in ks if d[k] is not None])
        q += f" WHERE {filters};"
        res = await self.execute(q)
        if res is None:
            return True
        n = int(res[7:])
        if n==0:
            return True
        return False

    async def update_or_insert(self, tbl, ks, d):
        ks = listify(ks)
        filters = {e:d[e] for e in ks}
        row = await self.select_one(tbl, filters=filters)
        if row is None:
            return await self.insert(tbl, d)
        return await self.update(tbl, ks, d)

    # Missing multi key delete
    async def delete(self, tbl, k, v):
        if k is None or v is None: return True
        q = f"DELETE FROM {tbl} WHERE {k}='{v}'"
        res = await self.execute(q)
        if res is None: return True
        n = int(res[7:])
        if n==0: return True
        return False
    
    async def get_seq(self, seqname):
        """ Return the next sequence value of the sequence seqname. """
        res = await self.query(f"select nextval('{seqname}')")
        return oget(res,[0,'nextval'])
    
    def set_seq(self, seqname):
        pass

    def update_stats(self):
        self.sync_query('vacuum analyze')

    def sync_startup(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.startup(*args, **kwargs))
    def sync_query(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.query(*args, **kwargs))
    def sync_select(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.select(*args, **kwargs))
    def sync_select_one(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.select_one(*args, **kwargs))
    def sync_insert(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.insert(*args, **kwargs))
    def sync_update(self,  *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.update(*args, **kwargs))
    def sync_update_or_insert(self,  *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.update_or_insert(*args, **kwargs))
    def sync_delete(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.delete(*args, **kwargs))
    def sync_get_seq(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.get_seq(*args, **kwargs))

# ####################################################################################################
# Utility DB functions
# ####################################################################################################

def row_to_rec(row, lcols):
    """
    Converts record dict extracted from db colapsing the id and name columns into dicts with id,name attrs for all cols with prefix lcols
    Example for lcols=['org']:
        {'id': 247, 'org_id': 3215,'org_name': 'RP'} -> {'id': 247, 'org': {'id': 3215, 'name': 'RP'}}
    """
    exclude = [f'{e}_id' for e in lcols] + [f'{e}_name' for e in lcols]
    rec = {k:row[k] for k in row if k not in exclude}
    for e in lcols:
        rec[e] = {'id':row[f'{e}_id'], 'name':row[f'{e}_name']}
    return rec

def rec_to_row(rec, lcols):
    """
    Converts recored into db row, colapsing the lookup dicts and ignoring the name attributes.
    Example for lcols=['org'] and record form row_to_rec() example:
        {'id': 247, 'org': {'id': 3215, 'name': 'RP'}} -> {'id': 247, 'org': 3215}
    """
    return {k:rec[k]['id'] if type(rec[k])==dict and k in lcols else rec[k] for k in rec}

def run_slq_cmds(db, q):
    for q in q.split(';'):
        if len(q)<10: continue
        db.sync_query(q+';')

def run_sql_file(db, fname):
    f = open(fname, 'r')
    qs = f.read()
    for q in [q for q in qs.split(";")]:
        db.sync_query(q)

def db_insert_df(db, tbl, df, dmap=None):
    if dmap is None:
        dmap={c:c for c in df.columns}
    else:
        df = df.rename(columns=dmap)
    cols = [dmap[c] for c in dmap]
    df = df[cols]
    for i in range(len(df)):
        row = df.iloc[i]
        d = {c:row[c] for c in cols}
        if db.sync_insert(tbl, d):
            print('DB insert error')
    return False

def log_and_return(msg):
    print(msg)
    return msg

def db_export_tbl(db, p, tbl):
    res = db.sync_select(tbl, limit=int(1e9))
    if res is None or not 'data' in res:
        return 1
    return pickle_save(p, res['data'])

def db_import_tbl(db, p, tbl, delete=False):
    p = Path(p)
    if not p.with_suffix('.pickle').is_file():
        return log_and_return(f'Error importing {tbl}: file {p} not found')
    rows = pickle_load(p)
    if rows is None:
        return log_and_return(f'Cant read {p}')
    if delete:
        if db.sync_query(f'delete from {tbl}'):
            return log_and_return(f'Error deleting tbl {tbl}')
    n = 0
    for row in rows:
        res = db.sync_insert(tbl, row)
        if res:
            return log_and_return(f'Error inserting record into {tbl}: {row}')
        n += 1
    print(f'Imported {n} records into {tbl}')
    return 0

def db_disable_serial(db, tbl, col):
    db.sync_query(f"alter table {tbl} alter column {col} drop default")

def db_enable_serial(db, tbl, col):
    n = db.sync_query(f"select max({col}) from {tbl}")[0]['max']
    db.sync_query(f"select pg_catalog.setval('public.{tbl}_{col}_seq', {n}, true)")
    db.sync_query(f"alter table {tbl} alter column {col} set default nextval('{tbl}_{col}_seq')")
