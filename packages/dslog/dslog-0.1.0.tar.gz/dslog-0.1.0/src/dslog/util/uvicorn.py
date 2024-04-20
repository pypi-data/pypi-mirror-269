def uvicorn_logconfig(prefix: str):
  return {
  "version": 1,
  "disable_existing_loggers": True,
  "formatters": {
    "custom": {
      "()": "uvicorn.logging.DefaultFormatter",
      "fmt": f"{prefix}%(levelprefix)s %(message)s",
      "use_colors": True
    },
  },
  "handlers": {
    "default": {
      "formatter": "custom",
      "class": "logging.StreamHandler",
      "stream": "ext://sys.stdout",
    },
  },
  "loggers": {
    "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False },
    "uvicorn.error": {"handlers": ["default"], "level": "INFO", "propagate": False },
    "uvicorn.access": {"handlers": ["default"], "level": "INFO", "propagate": False },
  }
  }