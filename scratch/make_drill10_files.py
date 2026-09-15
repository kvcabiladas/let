import os
import json

raw_items = [
    # --- Section 1 (Q1 to Q50) ---
    ("If a PE teacher observes a student raising both arms laterally, which plane of motion is being used?", ["Sagittal", "Frontal", "Transverse", "Oblique"], 1),
    ("During a high jump, a student bends backward to clear the bar. Which movement is primarily occurring at the spine?", ["Flexion", "Extension", "Rotation", "Lateral flexion"], 1),
    ("A marathon runner complains of fatigue after 30 km. Which metabolic process is predominantly used?", ["ATP-PCr", "Anaerobic glycolysis", "Aerobic oxidation of fats and carbohydrates", "Creatine phosphate"], 2),
    ("Which principle helps reduce injury during strength training?", ["No supervision", "Maximum weight at all times", "Skip warm-up and cool-down", "Gradual progression and proper form"], 3),
    ("A PE teacher wants to teach the Maglalatik dance safely in the classroom. Which modification is most appropriate?", ["Replace coconut shells with rubber bands", "Remove all percussion", "Perform seated only", "Skip the rhythm entirely"], 0),
    ("Which muscle group is the primary agonist during a squat?", ["Quadriceps", "Hamstrings", "Gastrocnemius", "Deltoids"], 0),
    ("Which method best develops both physical and cognitive skills simultaneously?", ["Drill practice", "Game-based practice", "Repetition only", "Isolated skill practice"], 1),
    ("A PE teacher uses a sit-and-reach test to measure students’ flexibility. Which body area is primarily assessed?", ["Quadriceps", "Hamstrings and lower back", "Gastrocnemius", "Shoulder girdle"], 1),
    ("Which type of footwear is most appropriate for minimizing lower limb injuries in running activities?", ["Supportive, well-cushioned, and sport-specific shoes", "Flip-flops or sandals", "Barefoot always", "High heels"], 0),
    ("A PE teacher monitors a student’s heart rate during moderate jogging. Which physiological principle explains the increased cardiac output?", ["Fick’s principle", "Overload principle", "SAID principle", "Law of inertia"], 0),
    ("Which pre-activity practice reduces the risk of musculoskeletal injuries?", ["Proper warm-up and stretching", "Heavy weightlifting without preparation", "Cold showers before activity", "Skipping warm-up"], 0),
    ("Which fitness test is most suitable for evaluating upper body muscular strength?", ["Push-up test", "Sit-and-reach test", "50-meter dash", "Beep test"], 0),
    ("Which Philippine festival is celebrated to honor the Santo Niño and includes street dancing with native costumes?", ["Pahiyas", "Panagbenga", "Kadayawan", "Sinulog"], 3),
    ("A student suffers an ankle inversion injury while playing basketball. Which ligament is most likely affected?", ["Deltoid ligament", "Anterior talofibular ligament", "Posterior tibiofibular ligament", "Plantar fascia"], 1),
    ("During folk dance instruction, what is the main focus for beginners?", ["Rhythm, timing, and cultural context", "Competitive performance only", "Improvisation without structure", "Speed and power"], 0),
    ("Which adaptation is appropriate for a student with hearing impairment during PE instruction?", ["Use visual demonstrations and gestures", "Avoid group activities", "Speak louder only", "Use only verbal instructions"], 0),
    ("A student-athlete performs better when praised individually rather than criticized publicly. Which psychological concept explains this?", ["Social facilitation", "Self-efficacy", "Motivation", "Individual differences"], 3),
    ("A volleyball player performs a spike. Which shoulder movement is predominantly used?", ["Flexion", "Abduction", "Internal rotation", "Horizontal adduction"], 3),
    ("According to Gentile’s taxonomy, a learner performing a free throw in a quiet gym is practicing which type of skill?", ["Closed skill with stationary object", "Open skill with moving object", "Closed skill with moving object", "Open skill with stationary object"], 0),
    ("Which of the following is the most common cause of overuse injuries in adolescents?", ["Repetitive movement with inadequate rest", "Accidental trauma", "Incorrect footwear only", "Playing outdoors"], 0),
    ("The inclusion of wellness education in PE reflects what modern shift?", ["Sports specialization", "Performance-based training", "Health-oriented curriculum", "Militaristic training"], 2),
    ("Which cardiorespiratory adaptation is expected after 12 weeks of aerobic training?", ["Decreased capillary density", "Decreased VO₂ max", "Increased stroke volume", "Decreased blood volume"], 2),
    ("During PE classes, which environment factor increases the risk of heat-related illnesses?", ["High temperature and humidity", "Moderate indoor temperature", "Shaded outdoor areas", "Hydration breaks"], 0),
    ("A coach uses observation and feedback to correct a student’s running form during practice. Which coaching method is being applied?", ["Demonstration", "Direct instruction", "Guided discovery", "Modeling"], 1),
    ("In volleyball, a ball touches the net on a serve but goes over into the opponent’s court. Which statement is correct?", ["The serve is a fault", "The serve is legal", "Point is replayed", "Serve is lost automatically"], 1),
    ("Which exercise principle ensures training mimics the movements of the sport for maximum performance improvement?", ["Reversibility", "Specificity", "Individualization", "Progression"], 1),
    ("A PE teacher integrates technology to monitor students’ heart rate during exercise. Which trend in physical education does this represent?", ["Use of wearable fitness technology", "Traditional calisthenics", "Playground games only", "Competitive sports exclusively"], 0),
    ("Which strategy enhances team cohesion in sports?", ["Regular team meetings and goal alignment", "Ignoring interpersonal conflicts", "Emphasizing only individual performance", "Reducing communication"], 0),
    ("Which principle ensures that training intensity, duration, and frequency are appropriate for the athlete’s current level?", ["Specificity", "Individualization", "Overload", "Progression"], 1),
    ("A school adopts yoga, tai chi, and mindfulness sessions to improve students’ mental health. Which trend is this?", ["Mind-body fitness integration", "Competitive athletics", "High-intensity interval training", "Traditional PE drills"], 0),
    ("Which factor is most important when designing safe and effective training sessions?", ["Athlete’s skill level and physical condition", "Coach’s personal preference", "Equipment brand", "Number of spectators"], 0),
    ("Which mental skill is most critical for athletes needing split-second decision-making under pressure?", ["Visualization", "Concentration", "Self-talk", "Relaxation"], 1),
    ("Which principle ensures that fitness tests accurately measure the intended component?", ["Validity", "Reliability", "Objectivity", "Standardization"], 0),
    ("Which principle of modern PE emphasizes personalized fitness programs based on student needs?", ["Ignoring student differences", "Mass drills for all", "Standardized workouts only", "Individualization and student-centered learning"], 3),
    ("A volleyball player repeatedly visualizes successful serves before matches. This technique primarily enhances:", ["Motivation", "Mental rehearsal", "Physiological adaptation", "Strength"], 1),
    ("A PE teacher observes a student performing a skill incorrectly during a competition but correctly during practice. Which factor explains this discrepancy?", ["Arousal and stress", "Fatigue", "Environmental temperature", "Motivation"], 0),
    ("A student performs high-intensity interval training (HIIT). Which system experiences the greatest adaptation?", ["ATP-PCr only", "Aerobic only", "Both anaerobic and aerobic", "None"], 2),
    ("Which goal-setting approach is most effective for improving athletic performance?", ["Outcome goals (winning a match)", "Process goals (focusing on technique)", "Performance goals (comparing to others)", "Avoidance goals (not losing)"], 1),
    ("During a basketball game, a player commits an illegal screen that blocks the defender’s path. Which infraction should the referee call?", ["Charging", "Blocking", "Holding", "Traveling"], 1),
    ("Which coping strategy is most effective for managing competition-related stress?", ["Avoidance", "Relaxation techniques and cognitive restructuring", "Ignoring stress", "Overtraining"], 1),
    ("During a sit-and-reach test, which muscles are being primarily assessed?", ["Quadriceps", "Hamstrings and lower back", "Gastrocnemius", "Gluteus maximus"], 1),
    ("A PE teacher uses verbal instructions and demonstrations repeatedly before practice. This primarily aids which type of learning?", ["Motor learning", "Perceptual learning", "Social learning", "Conceptual learning"], 0),
    ("Which type of feedback is most effective for beginners learning a new skill?", ["Intrinsic feedback only", "Extrinsic feedback with guidance", "Delayed feedback only", "Summary feedback only"], 1),
    ("Which energy system primarily fuels a 100-meter sprint lasting less than 15 seconds?", ["Phosphagen (ATP-PCr) system", "Anaerobic glycolysis", "Aerobic system", "Lactic acid system"], 0),
    ("Which of the following is a common characteristic of Philippine Muslim dances?", ["Performed in pairs only", "Heavy reliance on large props", "Fast foot-tapping only", "Use of fingers to express emotions"], 3),
    ("Which type of feedback is most beneficial during the early stages of skill learning?", ["Knowledge of results", "Knowledge of performance", "Intrinsic feedback only", "None"], 1),
    ("In a volleyball match, a player contacts the ball twice consecutively on a single play. Which is the correct ruling?", ["Legal play", "Fault, point for opponent", "Replay", "Allow continuation"], 1),
    ("Which principle explains progressive improvements in strength and endurance?", ["Overload principle", "Reversibility principle", "Specificity principle", "Individual differences principle"], 0),
    ("Which type of muscle fiber is best suited for short, explosive movements?", ["Type I (slow-twitch)", "Type IIa (fast-twitch oxidative)", "Type IIb (fast-twitch glycolytic)", "Type IIB (slow oxidative)"], 2),
    ("A coach encourages athletes to solve problems during practice rather than giving immediate solutions. This method emphasizes:", ["Guided discovery", "Direct instruction", "Repetition-based learning", "Drill practice"], 0),

    # --- Section 2 (Q51 to Q100) ---
    ("Which safety measure is most important for team sports with contact?", ["Ignoring rules", "Playing without supervision", "Use of protective gear and proper technique", "Allowing unsafe tackles"], 2),
    ("Which is the strongest justification for PE in national development?", ["Produces Olympic medalists", "Reduces healthcare costs", "Promotes celebrity athletes", "Encourages commercialization"], 1),
    ("A coach structures practice sessions to gradually increase difficulty over weeks. This demonstrates which principle?", ["Progression", "Overload", "Specificity", "Reversibility"], 0),
    ("If Physical Education is justified as essential because it develops the “whole person,” which concept is being emphasized?", ["Dualism", "Holism", "Mechanism", "Reductionism"], 1),
    ("Which factor contributes most to overtraining syndrome in athletes?", ["Excessive volume and intensity with inadequate rest", "Proper periodization", "Balanced diet", "Mental relaxation techniques"], 0),
    ("Which principle emphasizes providing physical education experiences tailored to students’ abilities?", ["Universal design", "Individualization", "Overload", "Specificity"], 1),
    ("In badminton, if a shuttle hits the net during a rally and lands on the opponent’s side, the correct ruling is:", ["Fault", "Let", "Point for the server", "Replay"], 2),
    ("A runner demonstrates excessive forward lean during sprinting. Which joint action primarily increases stride length?", ["Hip extension", "Knee flexion", "Ankle dorsiflexion", "Shoulder abduction"], 0),
    ("A PE teacher encourages positive self-talk in students to boost confidence. This intervention primarily targets:", ["Motivation", "Self-regulation", "Cognitive anxiety", "Arousal control"], 3),
    ("A gymnast practices mental imagery before routines. Which psychological outcome is primarily targeted?", ["Anxiety reduction and motor skill enhancement", "Muscular hypertrophy", "Aerobic endurance", "Flexibility"], 0),
    ("A student uses a wheelchair for mobility. Which PE modification is recommended?", ["Adapt games to include wheelchair mobility", "Exclude the student from running games", "Use only seated activities", "Require standing activities"], 0),
    ("Which of the following is critical for a PE teacher to maintain credibility as a game official?", ["Knowledge of rules", "Physical fitness", "Clear communication", "All of the above"], 3),
    ("A PE teacher ensures that the same protocol is used for all students during a test. Which principle is being applied?", ["Standardization", "Validity", "Reliability", "Objectivity"], 0),
    ("Which plane divides the body into superior and inferior parts, commonly used in rotational sports analysis?", ["Frontal", "Sagittal", "Transverse", "Oblique"], 2),
    ("A coach rotates players in different positions to develop versatility. Which coaching principle is being applied?", ["Transfer of learning", "Variability of practice", "Overload", "Specificity"], 1),
    ("Which physiological adaptation results from chronic endurance training?", ["Increased resting heart rate", "Increased stroke volume", "Decreased mitochondrial density", "Decreased capillary density"], 1),
    ("Which of the following best reflects the principle of progressive overload in fitness testing?", ["Gradually increasing test intensity over time", "Administering tests randomly", "Using only baseline tests", "Allowing unlimited rest during testing"], 0),
    ("A PE teacher designs a curriculum emphasizing lifelong fitness rather than competitive sports dominance. This approach best reflects which philosophical foundation?", ["Idealism", "Realism", "Pragmatism", "Existentialism"], 2),
    ("According to the inverted-U hypothesis, optimal performance occurs at:", ["Minimal arousal", "Moderate arousal", "Maximum arousal", "Zero arousal"], 1),
    ("Which dance originates from the Visayas and mimics the movements of a rooster?", ["Subli", "Tinikling", "Binislakan", "Kuratsa"], 3),
    ("A student experiences sudden chest pain while running. What is the first safety action?", ["Stop activity and call for medical help", "Encourage the student to continue", "Give water only", "Perform stretching"], 0),
    ("When PE promotes values such as teamwork and sportsmanship, it primarily addresses which domain?", ["Cognitive", "Psychomotor", "Affective", "Physiological"], 2),
    ("A school implements interactive fitness challenges using mobile apps, step counters, and gamified workouts. Which trend is being demonstrated?", ["Gamification and technology integration", "Traditional calisthenics", "Competition-only approach", "Teacher-led drills exclusively"], 0),
    ("A coach observes an athlete performing a skill incorrectly and uses demonstration with correction. Which learning method is being used?", ["Discovery learning", "Modeling", "Problem-solving", "Peer teaching"], 1),
    ("Which principle ensures fairness and impartiality in sports officiating?", ["Consistency and objectivity", "Bias toward the home team", "Ignoring infractions", "Allowing captain’s discretion"], 0),
    ("Which type of feedback helps athletes develop self-awareness and self-regulation during practice?", ["Extrinsic feedback only", "Intrinsic feedback", "Summary feedback only", "Delayed feedback"], 1),
    ("Which technology is commonly used for virtual or remote PE classes?", ["Chat room", "Dumbbells", "Chalk and blackboard", "Powerpoint"], 0),
    ("The K-12 curriculum’s inclusion of fitness components is aligned with which global health recommendation?", ["Olympic Charter", "WHO Physical Activity Guidelines", "ASEAN Education Framework", "UNESCO Arts Policy"], 1),
    ("Which motor milestone is expected around age 2–3 years?", ["Walking independently", "Skipping and hopping", "Running with arm-leg coordination", "Catching a small ball"], 0),
    ("A basketball player pivots on one foot while keeping the other in place. Which joint action occurs at the supporting hip?", ["Abduction", "Adduction", "Rotation", "Circumduction"], 2),
    ("A PE teacher notices that a 6-year-old child struggles with catching a large ball but can throw it easily. This difficulty is due to which developmental factor?", ["Fine motor skill deficit", "Gross motor skill imbalance", "Cognitive delay", "Visual-motor integration"], 3),
    ("Which assessment strategy is most appropriate for students with disabilities?", ["Flexible and criterion-referenced assessment", "Standardized testing only", "Time-based competition", "Excluding adaptive methods"], 0),
    ("A PE teacher notices that a child consistently performs a skill incorrectly due to previously learned habits. This is called:", ["Positive transfer", "Negative transfer", "Bilateral transfer", "Proactive inhibition"], 1),
    ("Which bone in the lower limb bears the most weight during running?", ["Femur", "Tibia", "Fibula", "Patella"], 1),
    ("Which approach in modern PE emphasizes health literacy and personal responsibility for wellness?", ["Fitness and wellness education", "Drill-based competition only", "Focus on winning games", "Ignoring health topics"], 0),
    ("A runner sets a goal to beat their personal best time in the next race. This is an example of:", ["Process goal", "Outcome goal", "Avoidance goal", "Extrinsic goal"], 1),
    ("If a PE program prioritizes measurable performance outputs only, what principle is neglected?", ["Inclusivity", "Efficiency", "Specificity", "Overload"], 0),
    ("Which approach emphasizes lifelong physical activity and wellness rather than competitive sports only?", ["Holistic physical education", "Drill-based instruction", "Competition-focused PE", "Weightlifting only"], 0),
    ("A basketball player misses free throws during finals but performs well in practice. Which psychological factor is most likely affecting performance?", ["Motivation", "Anxiety", "Self-efficacy", "Concentration"], 1),
    ("Which coaching behavior enhances long-term motivation and reduces burnout?", ["Positive reinforcement and constructive feedback", "Excessive criticism and pressure", "Ignoring effort", "Emphasizing only winning"], 0),
    ("A PE teacher emphasizes safety while performing Itik-itik. Which precaution is most suitable?", ["Ensure adequate space and avoid slippery floors", "Use elevated platforms", "Perform in small rooms only", "Skip footwork"], 0),
    ("During prolonged exercise, which macronutrient is the main energy source?", ["Protein", "Carbohydrates", "Fats", "Vitamins"], 1),
    ("The shift from militaristic drills during the American period to recreational physical activities in the Philippines reflects which educational movement?", ["Humanism", "Progressivism", "Perennialism", "Essentialism"], 1),
    ("Which type of motivation is driven by internal satisfaction rather than external rewards?", ["Intrinsic motivation", "Extrinsic motivation", "Achievement motivation", "Task-oriented motivation"], 0),
    ("Which type of periodization alternates high and low intensity across training cycles?", ["Linear", "Undulating", "Block", "Continuous"], 1),
    ("Which stage of motor learning is characterized by inconsistent performance and frequent errors?", ["Cognitive stage", "Associative stage", "Autonomous stage", "Retention stage"], 0),
    ("Which teaching method helps students retain cultural significance while performing folk dances?", ["Demonstration with explanation of history and symbolism", "Focus on speed and competition only", "Ignore traditional costumes", "Skip music and rhythm"], 0),
    ("A student trains at 60% of maximum heart rate for 45 minutes. Which component of fitness is primarily targeted?", ["Muscular strength", "Flexibility", "Aerobic endurance", "Agility"], 2),
    ("Which type of practice is most effective for skill acquisition in complex motor tasks?", ["Massed practice", "Distributed practice", "Random practice", "Blocked practice"], 2),
    ("A coach designs a training program emphasizing sport-specific movements. This primarily applies which principle?", ["Reversibility", "Specificity", "Overload", "Individualization"], 1),

    # --- Section 3 (Q101 to Q150) ---
    ("A PE teacher notes that a student has scapular winging. Which muscle is most likely weak?", ["Trapezius", "Serratus anterior", "Latissimus dorsi", "Rhomboids"], 1),
    ("Which hormone primarily regulates glucose mobilization during prolonged exercise?", ["Insulin", "Glucagon", "Cortisol", "Aldosterone"], 1),
    ("Which type of instruction is most effective for students with multiple disabilities?", ["Multi-sensory approach", "Verbal instructions only", "Competitive games only", "Standardized drills only"], 0),
    ("Which coaching style is most effective for highly skilled athletes seeking autonomy?", ["Authoritative", "Democratic", "Laissez-faire", "Command"], 1),
    ("Which is the primary oxygen-carrying molecule in blood?", ["Myoglobin", "Hemoglobin", "Albumin", "Fibrinogen"], 1),
    ("Which of the following is a closed kinetic chain exercise?", ["Leg extension machine", "Squat", "Biceps curl", "Bench press"], 1),
    ("A PE teacher promotes eco-friendly outdoor activities, like hiking and nature-based games. Which trend does this reflect?", ["Environmental and outdoor education in PE", "Indoor gym-based workouts only", "Competitive sports exclusively", "Weightlifting only"], 0),
    ("During skill retention tests, a student performs better after a period of rest. Which concept explains this phenomenon?", ["Transfer of learning", "Retention", "Generalization", "Repetition"], 1),
    ("A PE teacher wants to compare students’ aerobic fitness against national standards. Which term describes this approach?", ["Criterion-referenced testing", "Norm-referenced testing", "Formative assessment", "Summative assessment"], 0),
    ("A PE teacher modifies a relay race for students with mobility limitations. Which principle is being applied?", ["Adaptation for inclusion", "Progressive overload", "Specificity", "Reversibility"], 0),
    ("A school eliminates PE to give more time for Math and Science. From a philosophical standpoint, this decision contradicts which concept?", ["Education for specialization", "Education for utility", "Education for total development", "Education for efficiency"], 2),
    ("Which of the following is a responsibility of a PE teacher acting as a referee?", ["Enforcing rules", "Ensuring player safety", "Maintaining impartiality", "All of the above"], 3),
    ("A 10-year-old child exhibits rapid improvement in coordination but poor balance in new activities. This reflects which developmental principle?", ["Cephalocaudal", "Proximodistal", "Individual differences", "Maturation"], 3),
    ("A PE teacher explains offside rules in soccer. Which best describes offside?", ["Being nearer to the opponent’s goal than both the ball and second-last defender when receiving a pass", "Handling the ball intentionally", "Entering the field without permission", "Kicking the ball out of bounds intentionally"], 0),
    ("Which historical influence introduced structured physical drills in Philippine schools?", ["Spanish regime", "American regime", "Japanese regime", "Pre-colonial era"], 1),
    ("A coach emphasizes teamwork, discipline, and respect alongside technical skills. This reflects which coaching focus?", ["Holistic coaching", "Task-oriented coaching", "Outcome-oriented coaching", "Technical coaching only"], 0),
    ("Which type of joint allows the greatest range of motion in the human body?", ["Hinge", "Ball-and-socket", "Pivot", "Saddle"], 1),
    ("A student sprains their ankle during PE. Which is the recommended first aid approach?", ["Rest, Ice, Compression, Elevation (RICE)", "Immediate massage only", "Heat application immediately", "Continue activity"], 0),
    ("During a track and field race, an athlete steps inside the lane line and gains advantage. What is the proper ruling?", ["Warning", "Disqualification", "Time penalty", "Allow continuation"], 1),
    ("A student with visual impairment is learning to play goalball. Which modification enhances learning?", ["Use a ball with a bell inside", "Remove all sound cues", "Require outdoor play only", "Increase visual stimuli"], 0),
    ("A PE teacher implements hydration breaks, shaded areas, and pacing during outdoor activities. Which safety principle is being applied?", ["Environmental adaptation and risk management", "Overload principle", "Specificity principle", "None of the above"], 0),
    ("During the performance of the Tinikling, which motor skill is primarily required?", ["Agility and coordination", "Strength and power", "Flexibility only", "Endurance only"], 0),
    ("Which disability primarily requires modifications to enhance motor coordination and fine motor skills?", ["Intellectual disability", "Physical disability", "Visual impairment", "Hearing impairment"], 0),
    ("Which current trend focuses on inclusive PE for students of all abilities?", ["Traditional drill instruction", "Elite sports training only", "Gender-exclusive programs", "Adapted and inclusive physical education"], 3),
    ("A student experiences delayed onset muscle soreness (DOMS) after unaccustomed exercise. Which type of contraction caused it?", ["Concentric", "Eccentric", "Isometric", "Isokinetic"], 1),
    ("Which factor most influences the rate of motor development in children?", ["Practice only", "Genetics and environment", "Teacher motivation", "Equipment quality"], 1),
    ("A PE teacher officiating a soccer game notices a player deliberately handles the ball to prevent a goal. Which action should be taken?", ["Free kick for the defending team", "Goal awarded", "Penalty kick for the opposing team", "Throw-in"], 2),
    ("A PE teacher wants consistent results across multiple trials of a fitness test. Which principle is being emphasized?", ["Validity", "Reliability", "Objectivity", "Feasibility"], 1),
    ("A coach encourages self-assessment, reflection, and goal-setting in athletes. This approach emphasizes:", ["Athlete-centered coaching", "Drill-based coaching", "Command-style coaching", "Laissez-faire coaching"], 0),
    ("Which test is most appropriate for assessing lower body explosive power?", ["1-mile run", "Vertical jump", "Sit-and-reach", "Push-up"], 1),
    ("Which principle best supports including PE as a core subject in basic education?", ["Physical fitness improves academic performance", "Sports increase school revenue", "PE reduces classroom discipline issues", "PE prepares athletes for national competitions"], 0),
    ("Which principle states that children develop gross motor skills before fine motor skills?", ["Cephalocaudal", "Proximodistal", "Individual differences", "Maturation"], 1),
    ("A PE teacher observes that a student’s heart rate returns to baseline quickly after exercise. Which fitness component is being assessed?", ["Muscular endurance", "Flexibility", "Cardiovascular efficiency", "Agility"], 2),
    ("A PE teacher wants to modify a skill for a child with developmental delay. Which approach is most appropriate?", ["Reduce task complexity", "Increase task difficulty", "Remove visual cues", "Eliminate repetition"], 0),
    ("A student with cerebral palsy struggles with balance during locomotor activities. Which adaptation is most appropriate?", ["Reduce the activity space and provide support", "Eliminate movement activities", "Increase activity intensity", "Use competitive games only"], 0),
    ("During a push-up, which muscle is the primary stabilizer of the shoulder girdle?", ["Pectoralis major", "Triceps brachii", "Serratus anterior", "Deltoid"], 2),
    ("Which festival is celebrated in Baguio City and showcases flowers through street dancing?", ["Panagbenga", "Sinulog", "Kadayawan", "Ati-Atihan"], 0),
    ("Which best defines Physical Education as a discipline?", ["Training for athletes", "Study of human movement", "Military preparation", "Sports entertainment"], 1),
    ("Which test is most appropriate for assessing cardiovascular endurance in high school students?", ["1RM bench press", "20-meter shuttle run (Beep Test)", "Sit-and-reach test", "Vertical jump test"], 1),
    ("During exercise in hot environments, which physiological response prevents heat stroke?", ["Vasoconstriction", "Sweating and vasodilation", "Increased blood pressure", "Increased glycogen storage"], 1),
    ("A soccer team captain uses encouragement and verbal cues to maintain team cohesion. Which psychological principle is applied?", ["Leadership", "Self-confidence", "Goal setting", "Stress management"], 0),
    ("A PE teacher administers a fitness battery and records each student’s score. Which data type is primarily used?", ["Nominal", "Ordinal", "Interval/ratio", "Categorical"], 2),
    ("Which dance step in Cariñosa emphasizes handkerchief manipulation?", ["Balik-balik", "Cross-step", "Fan step", "Point-step"], 1),
    ("A teacher incorporates circuit training with strength, cardio, and flexibility stations. Which contemporary approach is being applied?", ["Functional fitness and cross-training", "Traditional single-skill drills", "Competitive game play only", "No structured plan"], 0),
    ("Which lever system is most commonly used in biceps curl exercises?", ["First-class", "Second-class", "Third-class", "None of the above"], 2),
    ("A PE teacher notices students performing exercises with poor form. Which preventive measure is most appropriate?", ["Provide proper instruction and supervision", "Ignore minor errors", "Encourage maximum load regardless of form", "Remove the exercise entirely"], 0),
    ("Which is a key goal of adapted physical education?", ["Promote lifelong physical activity and inclusion", "Focus solely on competition", "Limit participation to certain students", "Emphasize fitness testing only"], 0),
    ("A sprinter’s rapid arm swing during a race involves which type of muscle contraction?", ["Isometric", "Concentric", "Eccentric", "Static"], 1),
    ("During cycling, which joint action occurs at the knee when the pedal is pushed downward?", ["Flexion", "Extension", "Circumduction", "Lateral rotation"], 1),
    ("A child practices dribbling while moving unpredictably past obstacles. This is an example of:", ["Closed skill practice", "Open skill practice", "Isolated skill practice", "Stabilized skill practice"], 1)
]

os.makedirs('lib/data/bped_mock_test_1', exist_ok=True)

def generate_section(sec_id, start_idx, end_idx):
    sec_items = raw_items[start_idx:end_idx]
    code = f"import '../../models/question.dart';\n\n"
    code += f"const List<Question> bpedMockTest1Section{sec_id}Questions = [\n"
    
    for local_idx, (q_text, opts, corr_idx) in enumerate(sec_items):
        q_id = start_idx + local_idx + 1
        opts_formatted = ",\n      ".join([repr(o) for o in opts])
        code += f"  Question(\n"
        code += f"    id: {q_id},\n"
        code += f"    questionText:\n        {repr(q_text)},\n"
        code += f"    options: [\n      {opts_formatted},\n    ],\n"
        code += f"    correctAnswerIndex: {corr_idx},\n"
        code += f"  ),\n"
        
    code += "];\n"
    
    file_path = f"lib/data/bped_mock_test_1/bped_mock_test_1_section_{sec_id}.dart"
    with open(file_path, "w") as f:
        f.write(code)
    print(f"Generated {file_path} with {len(sec_items)} items.")

generate_section(1, 0, 50)
generate_section(2, 50, 100)
generate_section(3, 100, 150)

print("All 3 BPED Mock Test 1 section files successfully generated!")
