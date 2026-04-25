from core.models import Badge

def get_user_badges(user):
    """
    Calculates and returns a list of badges earned by the user based on their stats.
    """
    if not user.is_authenticated:
        return []

    # Calculate stats
    post_count = user.communitypost_set.count()
    comment_count = user.comment_set.count()
    scan_count = user.diagnostic_histories.count()
    
    # Simple logic: return all badges where required_count <= user's stat for that type
    earned_badges = []
    all_badges = Badge.objects.all().order_by('required_count')
    
    for badge in all_badges:
        stat_to_check = 0
        if badge.badge_type == 'post':
            stat_to_check = post_count
        elif badge.badge_type == 'comment':
            stat_to_check = comment_count
        elif badge.badge_type == 'scan':
            stat_to_check = scan_count
            
        if stat_to_check >= badge.required_count:
            earned_badges.append(badge)
            
    return earned_badges
