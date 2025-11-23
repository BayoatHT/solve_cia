# ────────────────────────────────────────────────────────────────────────────────────────────
# impact_titan\_logger\logger.py - Enhanced Production Logger
# Enterprise-grade logging with colors, icons, structured output, and agent tracking
# ────────────────────────────────────────────────────────────────────────────────────────────

import os
import sys
import json
import logging
import traceback
from datetime import datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from typing import Dict, Optional, Any
from proj_004_cia.__config.config import Config

# ────────────────────────────────────────────────────────────────────────────────────────────
# Enhanced Log Colors and Icons (Preserving your visual system)
# Professional icons and colors optimized for enterprise monitoring while maintaining readability
# ────────────────────────────────────────────────────────────────────────────────────────────
LOG_COLORS = {
    "DEBUG": "\033[94m",     # Blue - preserved for debugging
    "INFO": "\033[92m",      # Green - preserved for general info
    "SUCCESS": "\033[96m",   # Cyan - preserved for your success level
    "WARNING": "\033[93m",   # Yellow - preserved for warnings
    "ERROR": "\033[91m",     # Red - preserved for errors
    "CRITICAL": "\033[95m",  # Magenta - preserved for critical issues
    "AGENT": "\033[38;5;208m",    # Orange - new for agent activities
    "BUSINESS": "\033[38;5;141m",  # Purple - new for business logic
    "DATA": "\033[38;5;33m",      # Deep blue - new for data operations
    "ENDC": "\033[0m",       # Reset color - preserved
}

LOG_ICONS = {
    "DEBUG": "🔍",      # Magnifying glass for debugging
    "INFO": "ℹ️",       # Information symbol
    "SUCCESS": "✅",     # Check mark for success
    "WARNING": "⚠️",    # Warning triangle
    "ERROR": "❌",      # Cross mark for errors
    "CRITICAL": "🚨",   # Siren for critical issues
    "AGENT": "🤖",      # Robot for agent activities
    "BUSINESS": "📊",   # Chart for business operations
    "DATA": "📈",       # Data chart for data operations
    "SYSTEM": "⚙️",     # Gear for system operations
    "SECURITY": "🔒",   # Lock for security events
    "PERFORMANCE": "⚡",  # Lightning for performance metrics
}

# ────────────────────────────────────────────────────────────────────────────────────────────
# Custom Log Levels (preserving SUCCESS + adding enterprise levels)
# Extended logging levels for comprehensive enterprise monitoring
# ────────────────────────────────────────────────────────────────────────────────────────────
SUCCESS_LEVEL_NUM = 25  # Preserved - between INFO (20) and WARNING (30)
AGENT_LEVEL_NUM = 22    # New - for agent-specific logging
BUSINESS_LEVEL_NUM = 24  # New - for business logic events
DATA_LEVEL_NUM = 23     # New - for data pipeline events

logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")
logging.addLevelName(AGENT_LEVEL_NUM, "AGENT")
logging.addLevelName(BUSINESS_LEVEL_NUM, "BUSINESS")
logging.addLevelName(DATA_LEVEL_NUM, "DATA")


class EnhancedCustomLogger(logging.Logger):
    """
    Enhanced custom logger class with enterprise features
    Preserves all existing functionality while adding production capabilities
    """

    def __init__(self, name, level=logging.DEBUG):
        super().__init__(name, level)
        self.context_data = {}  # For structured logging context

    # ────────────────────────────────────────────────────────────────────────────────────────
    # Preserved Methods (maintaining exact same interface)
    # ────────────────────────────────────────────────────────────────────────────────────────
    def success(self, message, *args, **kwargs):
        """Custom log level for successful operations - PRESERVED"""
        # Extract context parameters that aren't for _log()
        context_params = {k: kwargs.pop(
            k) for k in ['agent_name', 'action', 'duration_ms'] if k in kwargs}
        if context_params:
            kwargs.setdefault('extra', {}).update(context_params)

        if self.isEnabledFor(SUCCESS_LEVEL_NUM):
            self._log(SUCCESS_LEVEL_NUM, message, args, **kwargs)

    # ────────────────────────────────────────────────────────────────────────────────────────
    # New Enterprise Methods (non-breaking additions)
    # ────────────────────────────────────────────────────────────────────────────────────────
    def agent(self, message, *args, agent_name=None, action=None, **kwargs):
        """Log agent-specific activities with context"""
        # Move context to extra dict
        context_params = {k: v for k, v in {
            'agent_name': agent_name, 'action': action}.items() if v is not None}
        if context_params:
            kwargs.setdefault('extra', {}).update(context_params)

        if self.isEnabledFor(AGENT_LEVEL_NUM):
            self._log(AGENT_LEVEL_NUM, message, args, **kwargs)

    def business(self, message, *args, division=None, function=None, **kwargs):
        """Log business logic events with context"""
        # Move context to extra dict
        context_params = {k: v for k, v in {
            'division': division, 'function': function}.items() if v is not None}
        if context_params:
            kwargs.setdefault('extra', {}).update(context_params)

        if self.isEnabledFor(BUSINESS_LEVEL_NUM):
            self._log(BUSINESS_LEVEL_NUM, message, args, **kwargs)

    def data(self, message, *args, source=None, records=None, **kwargs):
        """Log data pipeline activities with context"""
        # Move context to extra dict
        context_params = {k: v for k, v in {
            'data_source': source, 'record_count': records}.items() if v is not None}
        if context_params:
            kwargs.setdefault('extra', {}).update(context_params)

        if self.isEnabledFor(DATA_LEVEL_NUM):
            self._log(DATA_LEVEL_NUM, message, args, **kwargs)

    def performance(self, message, *args, duration=None, operation=None, **kwargs):
        """Log performance metrics with timing data"""
        extra_context = {"duration_ms": duration, "operation": operation}
        kwargs.setdefault('extra', {}).update(extra_context)
        self.info(f"⚡ PERFORMANCE: {message}", *args, **kwargs)

    def security(self, message, *args, user=None, action=None, **kwargs):
        """Log security events with user context"""
        extra_context = {"user": user, "security_action": action}
        kwargs.setdefault('extra', {}).update(extra_context)
        self.warning(f"🔒 SECURITY: {message}", *args, **kwargs)

    def set_context(self, **context):
        """Set persistent context data for all subsequent logs"""
        self.context_data.update(context)

    def clear_context(self):
        """Clear all context data"""
        self.context_data.clear()


class EnhancedColoredFormatter(logging.Formatter):
    """
    Enhanced formatter with icons, colors, and structured data
    Maintains visual appeal while adding enterprise context
    """

    def format(self, record):
        # ────────────────────────────────────────────────────────────────────────────────────
        # Preserve color system (your essential visual feedback)
        # ────────────────────────────────────────────────────────────────────────────────────
        log_color = LOG_COLORS.get(record.levelname, LOG_COLORS["ENDC"])
        reset_color = LOG_COLORS["ENDC"]
        icon = LOG_ICONS.get(record.levelname, "📋")

        # ────────────────────────────────────────────────────────────────────────────────────
        # Format base message (preserving your current format)
        # ────────────────────────────────────────────────────────────────────────────────────
        base_message = super().format(record)

        # ────────────────────────────────────────────────────────────────────────────────────
        # Add context information if available (enterprise enhancement)
        # ────────────────────────────────────────────────────────────────────────────────────
        context_parts = []

        # Agent context
        if hasattr(record, 'agent_name') and record.agent_name:
            context_parts.append(f"Agent:{record.agent_name}")
        if hasattr(record, 'action') and record.action:
            context_parts.append(f"Action:{record.action}")

        # Business context
        if hasattr(record, 'division') and record.division:
            context_parts.append(f"Division:{record.division}")
        if hasattr(record, 'function') and record.function:
            context_parts.append(f"Function:{record.function}")

        # Data context
        if hasattr(record, 'data_source') and record.data_source:
            context_parts.append(f"Source:{record.data_source}")
        if hasattr(record, 'record_count') and record.record_count:
            context_parts.append(f"Records:{record.record_count}")

        # Performance context
        if hasattr(record, 'duration_ms') and record.duration_ms:
            context_parts.append(f"Duration:{record.duration_ms}ms")
        if hasattr(record, 'operation') and record.operation:
            context_parts.append(f"Op:{record.operation}")

        # ────────────────────────────────────────────────────────────────────────────────────
        # Build enhanced message (preserving readability)
        # ────────────────────────────────────────────────────────────────────────────────────
        context_str = f" [{' | '.join(context_parts)}]" if context_parts else ""

        return f"{log_color}{icon} {base_message}{context_str}{reset_color}"


class StructuredFileFormatter(logging.Formatter):
    """
    JSON formatter for file logs (machine-readable for production monitoring)
    Enables integration with log aggregation systems like ELK stack
    """

    def format(self, record):
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add context data if available
        for attr in ['agent_name', 'action', 'division', 'function', 'data_source',
                     'record_count', 'duration_ms', 'operation', 'user', 'security_action']:
            if hasattr(record, attr):
                log_entry[attr] = getattr(record, attr)

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = traceback.format_exception(
                *record.exc_info)

        return json.dumps(log_entry, ensure_ascii=False)


def setup_enhanced_logger():
    """
    Enhanced logger setup preserving all current functionality
    Adds enterprise features without breaking existing usage
    Returns enhanced logger instance with backward compatibility
    """
    if not Config.LOGGING_ENABLED:
        return None

    # ────────────────────────────────────────────────────────────────────────────────────────
    # Ensure log directory exists (preserved logic)
    # ────────────────────────────────────────────────────────────────────────────────────────
    log_dir = os.path.join(os.path.dirname(Config.LOG_FILE_PATH), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(
        log_dir, os.path.basename(Config.LOG_FILE_PATH))

    # ────────────────────────────────────────────────────────────────────────────────────────
    # Register Enhanced Logger (preserving interface)
    # ────────────────────────────────────────────────────────────────────────────────────────
    logging.setLoggerClass(EnhancedCustomLogger)
    logger = EnhancedCustomLogger("ImpactTitanLogger", logging.DEBUG)

    # ────────────────────────────────────────────────────────────────────────────────────────
    # Enhanced File Handler with structured JSON logging
    # ────────────────────────────────────────────────────────────────────────────────────────
    if Config.ENVIRONMENT == "production":
        # Production: Time-based rotation + structured JSON
        file_handler = TimedRotatingFileHandler(
            log_file_path.replace('.log', '_structured.jsonl'),
            when='midnight',
            interval=1,
            backupCount=30,  # Keep 30 days
            encoding="utf-8"
        )
        file_handler.setFormatter(StructuredFileFormatter())
    else:
        # Development: Size-based rotation + readable format (preserved)
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=Config.LOG_FILE_SIZE_LIMIT,
            backupCount=Config.LOG_BACKUP_COUNT,
            encoding="utf-8"
        )
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ))

    file_handler.setLevel(logging.DEBUG)

    # ────────────────────────────────────────────────────────────────────────────────────────
    # Enhanced Console Handler (preserving your essential colors and format)
    # ────────────────────────────────────────────────────────────────────────────────────────
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, Config.LOG_LEVEL))

    # Use enhanced formatter with icons while preserving color system
    console_formatter = EnhancedColoredFormatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)

    # ────────────────────────────────────────────────────────────────────────────────────────
    # Add handlers (preserved structure)
    # ────────────────────────────────────────────────────────────────────────────────────────
    logger.addHandler(file_handler)
    if Config.LOG_CONSOLE_OUTPUT:
        logger.addHandler(console_handler)

    # ────────────────────────────────────────────────────────────────────────────────────────
    # Set global context for this session
    # ────────────────────────────────────────────────────────────────────────────────────────
    logger.set_context(
        environment=Config.ENVIRONMENT,
        version=Config.VERSION,
        system="impact_titan"
    )

    return logger


# ────────────────────────────────────────────────────────────────────────────────────────────
# Initialize Enhanced Logger (preserving variable name for backward compatibility)
# ────────────────────────────────────────────────────────────────────────────────────────────
app_logger = setup_enhanced_logger()

# ────────────────────────────────────────────────────────────────────────────────────────────
# Convenience Functions for Impact Titan Use Cases
# Enterprise-specific logging helpers for your distributed agent system
# ────────────────────────────────────────────────────────────────────────────────────────────


def log_agent_start(agent_name: str, action: str, context: Dict[str, Any] = None):
    """Log agent initialization with context"""
    if app_logger:
        context_str = f" with context: {context}" if context else ""
        app_logger.agent(f"Starting {action}{context_str}",
                         agent_name=agent_name, action=action)


def log_agent_success(agent_name: str, action: str, result: Any = None, duration: float = None):
    """Log successful agent completion"""
    if app_logger:
        result_str = f" → {result}" if result else ""
        perf_str = f" ({duration:.2f}ms)" if duration else ""

        # Build context in extra dict for proper logging
        extra_context = {"agent_name": agent_name, "action": action}
        if duration:
            extra_context["duration_ms"] = duration

        app_logger.success(f"Agent {agent_name} completed {action}{result_str}{perf_str}",
                           extra=extra_context)


def log_business_event(division: str, function: str, message: str, **context):
    """Log business function activities"""
    if app_logger:
        app_logger.business(message, division=division,
                            function=function, extra=context)


def log_data_operation(source: str, operation: str, record_count: int = None, **context):
    """Log data pipeline operations"""
    if app_logger:
        app_logger.data(f"{operation} from {source}",
                        source=source, records=record_count, extra=context)


def log_performance_metric(operation: str, duration_ms: float, **context):
    """Log performance measurements"""
    if app_logger:
        app_logger.performance(f"{operation} completed",
                               duration=duration_ms, operation=operation, extra=context)


def log_security_event(action: str, user: str = None, success: bool = True, **context):
    """Log security-related events"""
    if app_logger:
        status = "successful" if success else "failed"
        app_logger.security(f"{status} {action}",
                            user=user, action=action, extra=context)


# ────────────────────────────────────────────────────────────────────────────────────────────
# ENHANCED TESTING (preserving original tests + new features)
# ────────────────────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if app_logger:
        # ────────────────────────────────────────────────────────────────────────────────────
        # Original tests (preserved exactly)
        # ────────────────────────────────────────────────────────────────────────────────────
        app_logger.debug("This is a DEBUG message (used for deep debugging).")
        app_logger.info("This is an INFO message (used for general logs).")
        app_logger.success(
            "This is a SUCCESS message (indicates a task completed).")
        app_logger.warning(
            "This is a WARNING message (potential issue detected).")
        app_logger.error("This is an ERROR message (operation failed).")
        app_logger.critical("This is a CRITICAL message (severe failure).")

        # ────────────────────────────────────────────────────────────────────────────────────
        # New enterprise features demonstration
        # ────────────────────────────────────────────────────────────────────────────────────
        app_logger.agent("Initializing master orchestration",
                         agent_name="MasterAgent", action="startup")

        app_logger.business("Processing client classification",
                            division="marketing", function="client_analysis")

        app_logger.data("Ingesting World Bank economic indicators",
                        source="world_bank_api", records=1247)

        log_performance_metric("database_query", 245.7,
                               query_type="complex_join")

        log_security_event("api_access", user="system", success=True)

        # Test convenience functions
        log_agent_start("DataAgent", "world_bank_sync", {"region": "europe"})
        log_agent_success("DataAgent", "world_bank_sync",
                          "1,247 records processed", 3456.7)

        app_logger.success(
            "🚀 Enhanced logger testing completed - all systems operational!")
    else:
        print("Logging is disabled in configuration.")
