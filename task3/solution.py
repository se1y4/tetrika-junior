def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_start, lesson_end = intervals['lesson']
    
    def process_intervals(raw_intervals):
        times = []
        for i in range(0, len(raw_intervals), 2):
            start = raw_intervals[i]
            end = raw_intervals[i+1]
            if start >= end:
                continue
            times.append((start, end))
        times.sort()
        merged = []
        for start, end in times:
            if not merged:
                merged.append([start, end])
            else:
                last_start, last_end = merged[-1]
                if start <= last_end:
                    new_start = last_start
                    new_end = max(last_end, end)
                    merged[-1] = [new_start, new_end]
                else:
                    merged.append([start, end])
        clipped = []
        for start, end in merged:
            clipped_start = max(start, lesson_start)
            clipped_end = min(end, lesson_end)
            if clipped_start < clipped_end:
                clipped.append((clipped_start, clipped_end))
        return clipped
    
    pupil_intervals = process_intervals(intervals['pupil'])
    tutor_intervals = process_intervals(intervals['tutor'])
    
    total_time = 0
    i = j = 0
    while i < len(pupil_intervals) and j < len(tutor_intervals):
        pupil_start, pupil_end = pupil_intervals[i]
        tutor_start, tutor_end = tutor_intervals[j]
        
        overlap_start = max(pupil_start, tutor_start)
        overlap_end = min(pupil_end, tutor_end)
        
        if overlap_start < overlap_end:
            total_time += overlap_end - overlap_start
        
        if pupil_end < tutor_end:
            i += 1
        else:
            j += 1
    
    return total_time