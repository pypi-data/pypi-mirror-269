import secrets
import string
from datetime import datetime, timedelta

class API:
    def __init__(self):
        # Stores API keys and related data
        self.api_keys = {} # Example structure: {'key': {'user_id': '...', 'created_at': datetime, 'is_active': True, 'rate_limit': 100, 'calls_made': 0, 'reset_time': datetime}}
        
    def generate_api_key(self, user_id, rate_limit=100):
        key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(50))
        self.api_keys[key] = {
            'user_id': user_id,
            'created_at': datetime.now(),
            'is_active': True,
            'rate_limit': rate_limit,
            'calls_made': 0,
            'reset_time': datetime.now() + timedelta(hours=1) # Resets the rate limit every hour
        }
        return key
    
    def revoke_api_key(self, key):
        if key in self.api_keys:
            self.api_keys[key]['is_active'] = False
            return True
        return False
    
    def check_access_and_rate_limit(self, key):
        if key not in self.api_keys or not self.api_keys[key]['is_active']:
            return False, "Invalid or inactive API key"
        
        api_key_info = self.api_keys[key]
        if datetime.now() > api_key_info['reset_time']:
            api_key_info['calls_made'] = 0
            api_key_info['reset_time'] = datetime.now() + timedelta(hours=1)
        
        if api_key_info['calls_made'] < api_key_info['rate_limit']:
            api_key_info['calls_made'] += 1
            return True, "Access granted"
        else:
            return False, "Rate limit exceeded"
    
    def get_metrics_for_user(self, user_id):
        # Collect metrics for a specific user
        metrics = {'total_calls_made': 0, 'active_keys': 0}
        for key, info in self.api_keys.items():
            if info['user_id'] == user_id:
                metrics['total_calls_made'] += info['calls_made']
                if info['is_active']:
                    metrics['active_keys'] += 1
        return metrics

# Example usage
api = API()
user_id = "user123"
new_key = api.generate_api_key(user_id)
print("New API Key:", new_key)

access, message = api.check_access_and_rate_limit(new_key)
print("Access Check:", message)

metrics = api.get_metrics_for_user(user_id)
print("User Metrics:", metrics)

api.revoke_api_key(new_key)
print("API Key revoked:", not api.api_keys[new_key]['is_active'])