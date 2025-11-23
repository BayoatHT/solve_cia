# ────────────────────────────────────────────────────────────────────────────────────────────
# impact_titan\_config\config.py - Configuration Management
# Centralized configuration settings for the entire Impact Manager system
# ────────────────────────────────────────────────────────────────────────────────────────────
from dotenv import load_dotenv
from typing import Optional, Dict, List
from pathlib import Path
import os


# ────────────────────────────────────────────────────────────────────────────────────────────
# Load environment variables from .env file
# Automatically loads configuration from .env file in project root
# ────────────────────────────────────────────────────────────────────────────────────────────
load_dotenv()


class Config:
    """
    Main configuration class for Impact Manager
    Contains all system-wide settings and environment variables ordered by project importance
    """

    # ═══════════════════════════════════════════════════════════════════════════════════════
    # 1. PROJECT CORE SETTINGS - Essential project identity and structure
    # ═══════════════════════════════════════════════════════════════════════════════════════
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    PROJECT_NAME = "Impact Manager"
    VERSION = "0.1.0"
    SYSTEM_VERSION = "1.0.0"
    CONFIG_VERSION = "1.0.0"

    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG_MODE = os.getenv("DEBUG_MODE", str(
        ENVIRONMENT == "development")).lower() == "true"

    # ═══════════════════════════════════════════════════════════════════════════════════════
    # 2. SECURITY SETTINGS - Critical for enterprise deployment
    # ═══════════════════════════════════════════════════════════════════════════════════════
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # ═══════════════════════════════════════════════════════════════════════════════════════
    # 3. DATABASE CONFIGURATION - Data persistence foundation
    # ═══════════════════════════════════════════════════════════════════════════════════════
    # Development Database
    DEV_DB_HOSTNAME = os.getenv("DEV_DB_HOSTNAME", "localhost")
    DEV_DB_PORT = os.getenv("DEV_DB_PORT", "5432")
    DEV_DB_PASSWORD = os.getenv("DEV_DB_PASSWORD")
    DEV_DB_USERNAME = os.getenv("DEV_DB_USERNAME", "postgres")
    FASTAPI_DEV_DB_NAME = os.getenv("FASTAPI_DEV_DB_NAME", "fastapi")

    # Production Database
    US_PROD_DB_HOSTNAME = os.getenv("US_PROD_DB_HOSTNAME")
    US_PROD_DB_PORT = os.getenv("US_PROD_DB_PORT", "5432")
    US_PROD_DB_PASSWORD = os.getenv("US_PROD_DB_PASSWORD")
    US_PROD_DB_NAME = os.getenv("US_PROD_DB_NAME", "fastapi")
    US_PROD_DB_USERNAME = os.getenv("US_PROD_DB_USERNAME", "postgres")

    @classmethod
    def get_database_url(cls, environment="development"):
        """Get database URL based on environment"""
        if environment == "development":
            return f"postgresql://{cls.DEV_DB_USERNAME}:{cls.DEV_DB_PASSWORD}@{cls.DEV_DB_HOSTNAME}:{cls.DEV_DB_PORT}/{cls.FASTAPI_DEV_DB_NAME}"
        elif environment == "production":
            return f"postgresql://{cls.US_PROD_DB_USERNAME}:{cls.US_PROD_DB_PASSWORD}@{cls.US_PROD_DB_HOSTNAME}:{cls.US_PROD_DB_PORT}/{cls.US_PROD_DB_NAME}"
        else:
            return "sqlite:///impact_manager.db"

    # ═══════════════════════════════════════════════════════════════════════════════════════
    # 4. AI SERVICE API KEYS - Core AI functionality
    # ═══════════════════════════════════════════════════════════════════════════════════════
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    HUGGINGFACE_KEY = os.getenv("HUGGINGFACE_KEY")

    # ═══════════════════════════════════════════════════════════════════════════════════════
    # 5. LLM CONFIGURATION - AI behavior control
    # ═══════════════════════════════════════════════════════════════════════════════════════
    DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "gpt-4")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2000"))

    # ═══════════════════════════════════════════════════════════════════════════════════════
    # 6. AGENT SYSTEM SETTINGS - Distributed AI management
    # ═══════════════════════════════════════════════════════════════════════════════════════
    MAX_CONCURRENT_AGENTS = int(os.getenv("MAX_CONCURRENT_AGENTS", "10"))
    AGENT_TIMEOUT_SECONDS = int(os.getenv("AGENT_TIMEOUT_SECONDS", "300"))
    ENABLE_AGENT_CODE_MODIFICATION = os.getenv(
        "ENABLE_AGENT_CODE_MODIFICATION", "false").lower() == "true"

    # ═══════════════════════════════════════════════════════════════════════════════════════
    # 7. APPLICATION SETTINGS - Web service configuration
    # ═══════════════════════════════════════════════════════════════════════════════════════
    APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT = int(os.getenv("APP_PORT", "8000"))

    # ═══════════════════════════════════════════════════════════════════════════════════════
    # 8. LOGGING CONFIGURATION - System monitoring and debugging
    # ═══════════════════════════════════════════════════════════════════════════════════════
    LOGGING_ENABLED = os.getenv("LOGGING_ENABLED", "true").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FILE_SIZE_LIMIT = int(
        os.getenv("LOG_FILE_SIZE_LIMIT", "1048576"))  # 1MB
    LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))
    LOG_CONSOLE_OUTPUT = os.getenv(
        "LOG_CONSOLE_OUTPUT", "true").lower() == "true"

    # Fixed log paths
    LOGGER_FOLDER = f"C:\\Users\\bayoa\\impact_projects\\claude_solve_cia\\proj_004_cia\\__logger"
    LOG_FILE_PATH = f"{LOGGER_FOLDER}/logs/app.log"

    # ═══════════════════════════════════════════════════════════════════════════════════════
    # 9. DATA PIPELINE SETTINGS - Impact World System data processing
    # ═══════════════════════════════════════════════════════════════════════════════════════
    DATA_REFRESH_INTERVAL_HOURS = int(
        os.getenv("DATA_REFRESH_INTERVAL_HOURS", "24"))
    MAX_DATA_PROCESSING_WORKERS = int(
        os.getenv("MAX_DATA_PROCESSING_WORKERS", "4"))
    DATA_CACHE_TTL_SECONDS = int(os.getenv("DATA_CACHE_TTL_SECONDS", "3600"))

    # ═══════════════════════════════════════════════════════════════════════════════════════
    # 10. DATA SOURCE API KEYS - External data integration
    # ═══════════════════════════════════════════════════════════════════════════════════════
    # Financial Data
    FMP_API_KEY = os.getenv("FMP_API_KEY")  # Financial Modeling Prep
    FRED_API_KEY = os.getenv("FRED_API_KEY")  # Federal Reserve Economic Data

    # Global Impact Data
    WORLD_BANK_API_KEY = os.getenv("WORLD_BANK_API_KEY")
    WHO_API_KEY = os.getenv("WHO_API_KEY")
    UN_API_KEY = os.getenv("UN_API_KEY")

    # Government & Public Data
    CENSUS_API_KEY = os.getenv("CENSUS_API_KEY")
    NYC_OPEN_DATA_APP_TOKEN = os.getenv("NYC_OPEN_DATA_APP_TOKEN")

    # ═══════════════════════════════════════════════════════════════════════════════════════
    # 11. FRONTEND BUILD SETTINGS - SvelteKit generation system
    # ═══════════════════════════════════════════════════════════════════════════════════════
    FRONTEND_BUILD_PATH = os.getenv("FRONTEND_BUILD_PATH", "../frontend/build")
    SVELTE_OUTPUT_DIR = os.getenv("SVELTE_OUTPUT_DIR", "output/svelte_apps")

    # ═══════════════════════════════════════════════════════════════════════════════════════
    # 12. MONITORING & OBSERVABILITY - Production operations
    # ═══════════════════════════════════════════════════════════════════════════════════════
    ENABLE_METRICS = os.getenv("ENABLE_METRICS", "true").lower() == "true"
    METRICS_PORT = int(os.getenv("METRICS_PORT", "9090"))
    ALERT_EMAIL = os.getenv("ALERT_EMAIL")

    # ═══════════════════════════════════════════════════════════════════════════════════════
    # 13. COMMUNICATION SERVICES - External integrations
    # ═══════════════════════════════════════════════════════════════════════════════════════
    DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")  # Translation service
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # App-specific password

    # ═══════════════════════════════════════════════════════════════════════════════════════
    # 14. CLOUD INFRASTRUCTURE - Deployment and scaling
    # ═══════════════════════════════════════════════════════════════════════════════════════
    AWS_ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID")
    AWS_ACCOUNT_EMAIL = os.getenv("AWS_ACCOUNT_EMAIL")
    AWS_ACCOUNT_PASS = os.getenv("AWS_ACCOUNT_PASS")

    # ═══════════════════════════════════════════════════════════════════════════════════════
    # 15. IMPACT TITAN BUSINESS LOGIC - Core business categorization
    # ═══════════════════════════════════════════════════════════════════════════════════════
    USER_PERSONAS = [
        'concerned_citizen',
        'social_entrepreneur',
        'activist',
        'researcher',
        'organization',
    ]

    HUMANITARIAN_KEYS = [
        'no_poverty', 'zero_hunger', 'good_health_and_wellbeing', 'quality_education',
        'gender_equality', 'clean_water_and_sanitation', 'affordable_and_clean_energy',
        'decent_work_and_economic_growth', 'industry_innovation_and_infrastructure',
        'reduced_inequality', 'sustainable_cities_and_communities',
        'responsible_consumption_and_production', 'climate_action', 'life_below_water',
        'life_on_land', 'peace_justice_and_strong_institutions', 'partnerships_for_the_goals'
    ]

    CLIENT_KEYS = [
        'public_infrastructure',  # 1
        'corporate_social_responsibility',  # 2
        'agriculture_and_food',  # 3
        'government_agencies',  # 4
        'financial_institutions',  # 5
        'charities_and_ngos',  # 6
        'media_and_communications',  # 7
        'energy_and_utilities',  # 8
        'health_and_wellness',  # 9


        # ------------------------------------------------------------
        'charities',
        'non_profits_ngos',
        'educational_institutions',
        'social_enterprises_b_corps',
        'brands_with_purpose',
        'sustainability_businesses',
        'humanitarian_aid',
        'research_institutes',
        'startups_social_innovation',
        'environmental_advocacy',
        'social_impact_vc_firms',
        'philanthropic',
        'public_sector_agencies',
        'healthcare',
        'csr_programs',
        'political_campaigns'
    ]

    CONTROL_KEYS = [
        'machine_learning_model_development', 'performance_monitoring', 'developmental_evaluation',
        'business_intelligence_reporting', 'real_time_data_collection_tools', 'geospatial_program',
        'data_driven_program', 'participatory_action_planning', 'data_driven_research',
        'data_governance_compliance', 'initiative_audits', 'digital_marketing_strategy',
        'adaptive_management', 'mid_course_reviews', 'post_implementation_adjustments',
        'cost_effective_evaluation', 'data_visualization_services', 'swot_analysis',
        'data_engineering_services', 'real_time_feedback', 'llm_integration_services',
        'predictive_analytics_solutions'
    ]

    AWARENESS_KEYS = [
        'geotargeting', 'content_creation', 'seo', 'ppc_campaigns', 'web_design',
        'podcasts', 'social_media', 'influencer', 'pr_strategy', 'cause_based_event',
        'webinars', 'behavioral_data', 'video', 'email_marketing', 'community_engagement'
    ]

    RELEVANCE_KEYS = [
        'long_term_sustainability', 'needs_assessment', 'relevance_review', 'results_framework',
        'meta_evaluation', 'scenario_management', 'policy_monitoring', 'competitor_market',
        'stakeholder_alignment', 'theory_of_change', 'emerging_issues', 'portfolio_level',
        'global_impact', 'strategic_program'
    ]

    ENGAGEMENT_KEYS = [
        'social_media_strategy_influencer', 'email_engagement', 'crowdsourcing',
        'online_community', 'supporter_journey', 'seo_content', 'video_storytelling',
        'audience_segmentation', 'event_planning', 'paid_media_ppc_social',
        'volunteer_management', 'advocacy_training', 'loyalty_programs',
        'feedback_impact', 'grassroots_data', 'community_building', 'grassroots_survey',
        'digital_advocacy', 'community_polling', 'interactive_campaigns'
    ]

    # ═══════════════════════════════════════════════════════════════════════════════════════
    # 16. LANGUAGE & INTERNATIONALIZATION - Multi-language support
    # ═══════════════════════════════════════════════════════════════════════════════════════
    PRIMARY_LANGUAGES = {
        "en": "English", "es": "Spanish", "de": "German", "fr": "French", "it": "Italian",
        "ar": "Arabic", "bn": "Bengali", "fa": "Persian", "el": "Greek", "he": "Hebrew",
        "hi": "Hindi", "hu": "Hungarian", "id": "Indonesian", "ja": "Japanese",
        "ko": "Korean", "nl": "Dutch", "pl": "Polish", "pt": "Portuguese",
        "ru": "Russian", "sv": "Swedish", "tr": "Turkish", "uk": "Ukrainian",
        "ur": "Urdu", "vi": "Vietnamese", "zh": "Chinese (Simplified)", "zht": "Chinese (Traditional)"
    }

    WORLD_SYSTEM_LANGUAGES = {
        "en": "English", "es": "Spanish",
        "fr": "French", "it": "Italian",
        # ------------------------------------------------------------
        # "de": "German", "ar": "Arabic", "bn": "Bengali", "fa": "Persian", "el": "Greek",
        # "he": "Hebrew", "hi": "Hindi", "hu": "Hungarian", "id": "Indonesian",
        # "ja": "Japanese", "ko": "Korean", "nl": "Dutch", "pl": "Polish",
        # "pt": "Portuguese", "ru": "Russian", "sv": "Swedish","tr": "Turkish",
        # "uk": "Ukrainian", "ur": "Urdu", "vi": "Vietnamese",
        # "zh": "Chinese (Simplified)", "zht": "Chinese (Traditional)"
    }
    PREFERRED_LANGUAGES_UI = ['en', 'es', 'fr', 'it', 'de', 'pt']
    PREFERRED_LANGUAGES_MARKDOWN = ['en', 'es']
    LANGUAGE_CONTEXT = {
        "en": "Primary language for all content.",
        "es": "Secondary language with high demand for translations."
    }

    # ═══════════════════════════════════════════════════════════════════════════════════════
    # 17. SYSTEM RULES & TEMPLATES - Legacy system configurations
    # ═══════════════════════════════════════════════════════════════════════════════════════
    SYSTEM_TYPE_RULES = {
        "a_level_1_systems": {"operation": "recursive", "allow_learning": True, "shorthand": "level_1"},
        "b_level_2_systems": {"operation": "standard", "allow_learning": True, "shorthand": "level_2"},
        "c_level_3_systems": {"operation": "standard", "allow_learning": True, "shorthand": "level_3"},
        "d_level_4_systems": {"operation": "standard", "allow_learning": True, "shorthand": "level_4"},
        "e_md_level_2_systems": {"operation": "standard", "allow_learning": True, "shorthand": "md_level_2"},
        "f_md_level_3_systems": {"operation": "standard", "allow_learning": True, "shorthand": "md_level_3"},
        "g_auth_systems": {"operation": "recursive", "allow_learning": False, "shorthand": "auth"},
        "h_social_systems": {"operation": "recursive", "allow_learning": False, "shorthand": "social"},
        "i_util_systems": {"operation": "recursive", "allow_learning": False, "shorthand": "util"},
        "j_quotes_system": {"operation": "standard", "allow_learning": False, "shorthand": "quotes"}
    }

    FILE_TEMPLATE_REGISTRY = {
        "core": "c3a_partials_smc_core_components",
        "main": "c3c_partials_smc_main_components"
    }

    # ═══════════════════════════════════════════════════════════════════════════════════════
    # 18. FILE & FOLDER SETTINGS - Content management
    # ═══════════════════════════════════════════════════════════════════════════════════════
    MARKDOWN_EXTENSION = ".md"
    PYTHON_EXTENSION = ".py"
    IMAGE_EXTENSIONS = [".jpg", ".png", ".webp"]

    CATEGORY_MARKDOWN_FOLDER_SUFFIX = "_md"
    TRANSLATIONS_FOLDER = "Translations"
    MISSED_FOLDER = "Missed"
    ORIGINAL_FOLDER = "Original"

    DEFAULT_STRUCTURE = {"Original": {}, "Translations": {"Missed": {}}}
    DEFAULT_TRANSLATION_FOLDER_STRUCTURE = {"Original": {
        "Details": {}}, "Translations": {"Missed": {"Details": {}}}}

    # ═══════════════════════════════════════════════════════════════════════════════════════
    # 19. UTILITY SETTINGS - Miscellaneous configurations
    # ═══════════════════════════════════════════════════════════════════════════════════════
    DEFAULT_IMAGE_SIZE = 500
    RESERVED_KEYS = ["all", "none", "default", "missed", "original"]
    SECTION_EXTRAS = {
        "services": ["clients", "works", "impacts"],
        "clients": ["services", "goals", "challenges"]
    }

    # ═══════════════════════════════════════════════════════════════════════════════════════
    # UTILITY METHODS
    # ═══════════════════════════════════════════════════════════════════════════════════════
    @classmethod
    def validate_required_settings(cls) -> bool:
        """Validates that all required configuration settings are present"""
        required_settings = ["SECRET_KEY"]
        missing_settings = []
        for setting in required_settings:
            if not getattr(cls, setting) or getattr(cls, setting) == "your-secret-key-change-this":
                missing_settings.append(setting)

        if missing_settings:
            raise ValueError(
                f"Missing required configuration settings: {missing_settings}")
        return True

    @classmethod
    def get_log_file_path(cls) -> Path:
        """Returns the absolute path for the log file"""
        log_dir = cls.PROJECT_ROOT / "logs"
        log_dir.mkdir(exist_ok=True)
        return log_dir / "app.log"

    @classmethod
    def get_data_directory(cls) -> Path:
        """Returns the data directory path"""
        data_dir = cls.PROJECT_ROOT / "data"
        data_dir.mkdir(exist_ok=True)
        return data_dir

    @classmethod
    def get_output_directory(cls) -> Path:
        """Returns the output directory for generated content"""
        output_dir = cls.PROJECT_ROOT / "output"
        output_dir.mkdir(exist_ok=True)
        return output_dir

    @staticmethod
    def normalize_path(path: str) -> str:
        """Normalizes file path for cross-platform compatibility"""
        return os.path.normpath(path)
