import logging

def setup_logging():
    #------------------------------------------------
    # *              setup_logging
    # ?  This method sets up the logging configuration
    # @param output_log_file type str  
    # @return type logging.Logger
    #------------------------------------------------
    
    #---------------------------
    #     Logging Configuration
    #---------------------------
    logger = logging.getLogger('app_log')
        
    logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers(): 
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #---------------------------
        #     Logging Handlers
        #---------------------------
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

        logger.info("Logging setup complete - INFO level and above will be logged to console.")
    
    return logger