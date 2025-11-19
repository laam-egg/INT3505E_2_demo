from .basic import log

def audit(action, user="anonymous", detail=None):
    log.msg("audit", action=action, user=user, detail=detail)
