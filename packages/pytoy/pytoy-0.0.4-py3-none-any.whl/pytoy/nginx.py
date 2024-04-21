from common import *


class Nginx:
    def installed(self) -> bool:
        """Check if Nginx is installed"""
        return bool(run_command_str("which nginx"))

    def version(self) -> str:
        """Get Nginx version"""
        return run_command_str("nginx -v")
    
    def log_error(self) -> str:
        """Get Nginx log"""
        return run_command_str("cat /var/log/nginx/error.log")
    
    def config(self) -> str:
        """Get Nginx config"""
        return run_command_str("nginx -T")
    
    def reload(self) -> str:
        """Reload Nginx"""
        return run_command_str("nginx -s reload")
    
    def restart(self) -> str:
        """Restart Nginx"""
        return run_command_str("nginx -s reopen")
