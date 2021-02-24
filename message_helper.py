def check_channel_id(channels, channel_id):
    '''
    Given a list of authorised channels for a user,
    check if channel_id is in the list of authorised channels
    Returns 1 if authorised, else 0
    '''
    for i in channels:
        if i == channel_id:
            return 1
    
    return 0