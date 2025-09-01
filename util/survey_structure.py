MOTIVATION_LIKERT_COLUMNS = ['boring_task', 'enjoyable_task', 'satisfied_performance',
       'couldnt_do_well', 'effort_task', 'didnt_try_hard', 'felt_tense',
       'relaxed_task', 'help_memorize_commands', 'ability_matched_difficulty',
       'attention', 'interesting_things', 'genuine_pride',
       'intuitive_controls', 'total_control', 'time_alter',
       'aware_performance', 'no_effort_focus', 'not_worried_performance',
       'spontaneous_automatic', 'goals_defined', 'MentalDemand',
       'PhysicalDemand', 'TemporalDemand', 'Performance', 'Effort',
       'Frustration', 'Accuracy', 'Speed', 'LearningEffort', 'Learning']

MOTIVATION_8_PART_COLUMNS = ['already_memorized', 'dont_want_to_continue','boring_task', 'satisfied_performance','effort_task', 'relaxed_task','help_memorize_commands']

MOTIVATION_8_PART_STATEMENTS = {
    'already_memorized': "I would skip further training because I have already memorized the locations.",
    'dont_want_to_continue': "I would skip further training because I do not want to continue doing this task.",
    'boring_task': "I thought this was a boring task.",
    'satisfied_performance': "I am satisfied with my performance at this task.", 
    'effort_task': "I put a lot of effort into this task.",
    'relaxed_task': "I was very relaxed in doing this task.",
    'help_memorize_commands': "I think doing this task could help me to memorize the locations of useful commands when I'm using complex software."
}


MOTIVATION_SHORT_LIKERT_COLUMNS = ['boring_task', 'enjoyable_task', 'satisfied_performance',
       'couldnt_do_well', 'attention', 'effort_task', 'didnt_try_hard',
       'felt_tense', 'relaxed_task', 'help_memorize_commands',  'engagement']  #'skip_remaining_training']


MOTIVATION_STATEMENTS = {
    "boring_task": "I thought this was a boring task.",
    "enjoyable_task": "I thought this task was quite enjoyable.",
    "satisfied_performance": "I am satisfied with my performance at this task.",
    "couldnt_do_well": "This was a task that I couldn't do very well.",
    "effort_task": "I put a lot of effort into this task.",
    "didnt_try_hard": "I didn't try very hard to do well at this task.",
    "felt_tense": "I felt very tense while doing this task.",
    "relaxed_task": "I was very relaxed in doing this task.",
    "help_memorize_commands": "I think doing this task could help me to memorize the locations of useful commands when I'm using complex software.",
    "ability_matched_difficulty": "My ability to do this task is well matched with the difficulty of the task.",
    "attention": "Select the rightmost value (Strongly Agree). This is an attention check.",
    "interesting_things": "I was able to do interesting things within the task.",
    "genuine_pride": "When I accomplished something in the task I experienced genuine pride.",
    "intuitive_controls": "The task controls are intuitive.",
    "total_control": "I felt in total control while doing this task.",
    "time_alter": "Time seemed to alter (either slowed down or sped up) while I was completing this task.",
    "aware_performance": "I was aware of how well I was performing in the task.",
    "no_effort_focus": "It was no effort to keep my mind on what was happening.",
    "not_worried_performance": "I was not worried about how well I was doing at the task.",
    "spontaneous_automatic": "I did things spontaneously and automatically without having to think.",
    "goals_defined": "My goals in this task were clearly defined.",
    "MentalDemand": "This task was mentally demanding.",
    "PhysicalDemand": "This task was physically demanding.",
    "TemporalDemand": "I felt hurried or rushed while completing this task.",
    "Performance": "I was successful in accomplishing what I was asked to do.",
    "Effort": "I had to work very hard to accomplish my level of performance.",
    "Frustration": "I felt insecure, discouraged, irritated, stressed and annoyed during this task.",
    "Accuracy": "I was able to be accurate in these tasks.",
    "Speed": "I was able to complete these tasks quickly",
    "LearningEffort": "I put effort into learning and remembering the icon locations.",
    "Learning": "I learned the icon locations.",
#     "skip_remaining_training": "If I was completing this training session to learn the icon locations in a real software interface, I would skip the rest of the training at this point."
    "engagement": "If I was completing this training session to learn the icon locations in a real software interface, I would skip the rest of the training at this point."

}