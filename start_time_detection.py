def will_catch(df, prev_event, curr_event, start_prev, start_curr, x=0.1, y=0.1):
    """
    Determine if the fastest x% of curr_event will catch the slowest y% of prev_event.

    Parameters:
    - df: pandas.DataFrame with columns ['event', 'pace', 'distance'].
    - prev_event: name of the preceding event.
    - curr_event: name of the upcoming event.
    - start_prev, start_curr: start times in minutes from midnight (e.g., 7*60 for 07:00).
    - x: fraction (0-1) of fastest runners in curr_event.
    - y: fraction (0-1) of slowest runners in prev_event.

    Returns:
    - will_catch_flag (bool): True if catch occurs before the preceding event distance.
    - catch_distance (float): km at which the catch occurs (None if no catch).
    - catch_time (float): time in minutes from midnight when the catch occurs (None if no catch).
    """
    # Extract pace/distribution
    prev = df[df['event'] == prev_event]
    curr = df[df['event'] == curr_event]

    if prev.empty or curr.empty:
        raise ValueError("Event names not found in dataframe.")

    # Compute pace thresholds
    p_prev_slosest = prev['pace'].quantile(1 - y)
    p_curr_fastest = curr['pace'].quantile(x)

    # Head start time difference
    head_start = start_curr - start_prev

    # If slower runner is actually faster or equal, no catch
    denom = p_prev_slosest - p_curr_fastest
    if denom <= 0:
        return False, None, None

    # Distance at which catch happens
    catch_distance = head_start / denom

    # Shared course distance (preceding event distance)
    shared_distance = prev['distance'].iloc[0]

    # Determine if catch happens before the preceding event finishes
    will_catch_flag = catch_distance <= shared_distance

    # Time since curr_event start when catch occurs
    catch_time_since_curr = catch_distance * p_curr_fastest
    catch_time = start_curr + catch_time_since_curr

    return will_catch_flag, catch_distance, catch_time
