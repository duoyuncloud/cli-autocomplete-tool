# core/cache_manager.py
"""
Caching layer for frequently used completions.
"""

import json
import os
import time
from typing import Dict, List, Optional, Any
from pathlib import Path


class CacheManager:
    """Manages caching of completion suggestions for performance."""
    
    def __init__(self, cache_dir: Optional[str] = None, max_size: int = 1000):
        """
        Initialize cache manager.
        
        Args:
            cache_dir: Directory to store cache files (default: ~/.cli_autocomplete)
            max_size: Maximum number of cached entries
        """
        if cache_dir is None:
            cache_dir = os.path.expanduser("~/.cli_autocomplete")
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.max_size = max_size
        self.cache_file = self.cache_dir / "completion_cache.json"
        self.cache: Dict[str, Dict[str, Any]] = {}
        self._load_cache()
    
    def _load_cache(self):
        """Load cache from disk."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    self.cache = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.cache = {}
        else:
            self.cache = {}
    
    def _save_cache(self):
        """Save cache to disk."""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except IOError:
            # Silently fail if we can't save cache
            pass
    
    def _cleanup_cache(self):
        """Remove old entries if cache is too large."""
        if len(self.cache) > self.max_size:
            # Sort by last_used and remove oldest entries
            sorted_items = sorted(
                self.cache.items(),
                key=lambda x: x[1].get('last_used', 0)
            )
            # Keep only the most recent entries
            self.cache = dict(sorted_items[-self.max_size:])
    
    def get(self, key: str) -> Optional[List[str]]:
        """
        Get cached suggestions for a key.
        
        Args:
            key: Cache key (usually command context)
            
        Returns:
            Cached suggestions or None if not found
        """
        if key in self.cache:
            entry = self.cache[key]
            # Update last used time
            entry['last_used'] = time.time()
            entry['hit_count'] = entry.get('hit_count', 0) + 1
            return entry.get('suggestions', [])
        return None
    
    def set(self, key: str, suggestions: List[str], ttl: int = 3600):
        """
        Cache suggestions for a key.
        
        Args:
            key: Cache key (usually command context)
            suggestions: List of suggestions to cache
            ttl: Time to live in seconds (default: 1 hour)
        """
        self.cache[key] = {
            'suggestions': suggestions,
            'created': time.time(),
            'last_used': time.time(),
            'hit_count': 0,
            'ttl': ttl
        }
        self._cleanup_cache()
        self._save_cache()
    
    def invalidate(self, key: str):
        """Remove a specific key from cache."""
        if key in self.cache:
            del self.cache[key]
            self._save_cache()
    
    def clear(self):
        """Clear all cached entries."""
        self.cache = {}
        self._save_cache()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_entries = len(self.cache)
        total_hits = sum(entry.get('hit_count', 0) for entry in self.cache.values())
        
        return {
            'total_entries': total_entries,
            'total_hits': total_hits,
            'cache_size': total_entries,
            'max_size': self.max_size
        }
    
    def cleanup_expired(self):
        """Remove expired entries from cache."""
        current_time = time.time()
        expired_keys = []
        
        for key, entry in self.cache.items():
            created = entry.get('created', 0)
            ttl = entry.get('ttl', 3600)
            if current_time - created > ttl:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            self._save_cache()


# Global cache instance
_cache_manager: Optional[CacheManager] = None


def get_cache_manager() -> CacheManager:
    """Get or create global cache manager instance."""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager


def cache_suggestions(key: str, suggestions: List[str], ttl: int = 3600):
    """Convenience function to cache suggestions."""
    cache_manager = get_cache_manager()
    cache_manager.set(key, suggestions, ttl)


def get_cached_suggestions(key: str) -> Optional[List[str]]:
    """Convenience function to get cached suggestions."""
    cache_manager = get_cache_manager()
    return cache_manager.get(key) 