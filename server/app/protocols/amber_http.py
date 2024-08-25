import requests
import logging

from models import FlagStatus, SubmitResult

logger = logging.getLogger(__name__)

RESPONSES = {
    FlagStatus.QUEUED: ['timeout', 'game not started', 'try again later', 'game over', 'is not up',
                        'no such flag'],
    FlagStatus.ACCEPTED: ['accepted', 'congrat'],
    FlagStatus.REJECTED: ['bad', 'wrong', 'expired', 'unknown', 'your own',
                          'too old', 'not in database', 'already submitted', 'invalid flag'],
}

TIMEOUT = 5

def submit_flags(flags, config):
    flag_list = [item.flag for item in flags]
    
    r = requests.post(config['SYSTEM_URL'], json={ "flags": flag_list }, timeout=TIMEOUT)
    accepted_flags = r.json()['accepted']
    
    for flag in flag_list:
        if flag in accepted_flags:
            yield SubmitResult(flag, FlagStatus.ACCEPTED, "accepted")
        else:
            yield SubmitResult(flag, FlagStatus.REJECTED, "rejected")
