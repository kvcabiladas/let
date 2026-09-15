import os
import json

# 150 questions for BPED Specialization Drill 4 - Sports Part 2
raw_items = [
    # --- Section 1 (Q1 to Q50) ---
    ("Which of the following statements is TRUE about Patintero?", ["It is played on a square field.", "The team with the most tagged incidents wins.", "The game is played outdoors, day or night.", "The runners are the ones who block the taggers."], 2),
    ("In the game Palo Sebo, what is the main objective?", ["To knock down the bamboo pole.", "To climb the slippery pole and retrieve the prize at the top.", "To be the fastest runner.", "To knock off other players while climbing."], 1),
    ("In Sunka, how is the winner determined?", ["The player who retrieves the most sigays.", "The player who runs out of sigays first.", "The player who retrieves the flag at the top of the board.", "The player who has the greatest number of sigays."], 3),
    ("Which traditional Filipino game is similar to the piñata?", ["Sunka", "Luksong Tinik", "Pukpok Palayok", "Palo Sebo"], 2),
    ("What happens if a player touches the obstacle in Luksong Tinik?", ["They continue playing without penalty.", "They are disqualified from the game.", "The ‘mother’ tries to jump on their behalf.", "The player becomes the ‘it.’"], 2),
    ("Where did the game Luksong Baka originate?", ["Bulacan", "Cebu", "Davao", "Manila"], 0),
    ("How many players are required for the game Patintero in one version?", ["4 players", "6 players", "8 players", "10 players"], 1),
    ("What is the consequence of failing to climb the bamboo pole in Palo Sebo?", ["The player gets another chance.", "The player is disqualified.", "The prize is removed.", "The game is restarted."], 1),
    ("In Patintero, what strategic advantage does a team have by placing their taggers along specific sections of the rectangular field?", ["It forces the runners to slow down and increases the chances of being tagged.", "It allows the taggers to switch roles with the runners easily.", "It helps the runners score more points by advancing quickly.", "It makes it easier for the taggers to hide from the runners."], 0),
    ("In Palo Sebo, why is the bamboo pole often polished and greased with oil?", ["To prevent players from using tools to climb the pole.", "To increase the difficulty by making it slippery for climbers.", "To ensure the pole remains durable for longer contests.", "To allow the flag or prize to move down more easily."], 1),
    ("In the game of Sunka, how does the \"last sigay\" placement influence the player's next move?", ["The player loses all their sigays if the last sigay is placed in an empty hole.", "The player can immediately capture all sigays in the opponent's row if the last sigay lands in their big hole.", "The player gets to continue their turn if the last sigay is placed in their big hole.", "The game ends if the last sigay is placed in a hole with no remaining sigays."], 2),
    ("What role does the crowd play in Pukpok Palayok, and how does it affect the player's ability to hit the pot?", ["The crowd intentionally misguides the player, making it harder for them to hit the pot.", "The crowd stays silent to maintain fairness, preventing distractions.", "The crowd provides verbal guidance to help the player locate the pot.", "The crowd is responsible for determining the player’s next move based on their strategy."], 2),
    ("In Luksong Tinik, what happens if the ‘mother’ successfully jumps over the stacked fingers after the ‘child’ fails?", ["The child gets another chance to jump.", "The team avoids becoming the ‘it’ and continues the game.", "Both players switch to the role of ‘it’.", "The stack is lowered to make it easier for the next round."], 1),
    ("In Patintero, which specific movement strategy could increase a runner’s chances of evading the taggers?", ["Running as fast as possible without considering the position of the taggers.", "Pausing mid-run to confuse the taggers before making a sudden dash.", "Moving in a straight line without changing direction to reduce the risk of slipping.", "Attempting to outrun all taggers by staying close to the boundary lines."], 1),
    ("What specific skill is emphasized in Palo Sebo that separates successful climbers from those who fail to reach the top?", ["Physical strength to grip the pole tightly.", "Mental focus to calculate each movement.", "Speed in ascending the pole before it becomes too slippery.", "Coordination of teamwork to push each other up the pole."], 1),
    ("Which of the following best describes a key rule in the game \"Kadang-Kadang\" that contributes to a player's disqualification?", ["The player must maintain their balance while walking on 10-foot bamboo stilts and cannot fall more than once before reaching the finish line.", "The player must start running as soon as the signal \"Go\" is given and reach the 25th-meter mark without stepping off the stilts.", "If a player falls off the stilts twice or steps off the stilts after taking two steps, they are disqualified from the race.", "Players must walk towards the finish line on 5-foot bamboo stilts, and any player who steps off before reaching the 50-meter mark is disqualified."], 2),
    ("In the game Karera ng Baong Sangko, what is the primary equipment used by players?", ["Bamboo stilts", "Coconut shells with abaca string", "Wooden stilts with rubber grips", "Plastic shells with nylon ropes"], 1),
    ("In Luksong Lubid (jump rope), how is the game typically played?", ["Players run on coconut shell stilts towards the finish line.", "Players jump over a bamboo pole raised higher after each round.", "Two players swing the rope, and another player jumps until they touch the rope with their feet.", "Players walk on bamboo stilts without falling until they reach the 25th-meter mark."], 2),
    ("In Kadang-Kadang, what happens when a player falls off the bamboo stilts twice before reaching the finish line?", ["The player must restart from the beginning.", "The player is given one more chance to continue.", "The player is considered \"OUT\" or disqualified.", "The player must sit out until the next round."], 2),
    ("In Karera ng Baong Sangko, how is the rope used by the players prepared?", ["The rope is wrapped around the coconut shells and tied tightly.", "The abaca rope is inserted into the eyes of the coconut shells and measured to the height of the user.", "The rope is placed over the player’s shoulders to pull the stilts forward.", "The rope is attached to the finish line to mark the end of the race."], 1),
    ("In playing sungka, how many houses each player has in front of him?", ["7", "12", "5", "10"], 0),
    ("What is/are the difference between Hampas Palayok and Mexican Piñata?", ["Hampas palayok has many participants while is Peñata played by few.", "One use stick while other uses hands", "Pinata uses candy, while hampas palayok uses peso bills.", "Hamplas palayok is made from jars and Piñata is made of paper mache or cloth."], 3),
    ("What will happen if the player fails to climb the pole and falls during a Palo Sebo game?", ["Player will repeat to climb", "He will pass the flag to opponent", "He cannot longer climb", "He is automatically lost"], 3),
    ("What is the main objective of the Kadang-Kadang race?", ["To jump the highest on bamboo stilts", "To reach the finish line while maintaining balance and agility", "To perform tricks while walking on stilts", "To knock over the opposing team using bamboo stilts"], 1),
    ("What are the compare and contrasting ideas of LUKSONG TINIK and LUKSONG BAKA?", ["Both are examples of outdoor play", "Both can be played inside the house.", "Both require jumping but differ on what is used; luksong tinik uses fingers, while luksong baka needs to jump over an arched back.", "Both require jumping but differ on what is used; luksong tinik needs to jump over an arched back, while luksong baka uses fingers."], 2),
    ("What was the critical historical development that shifted swimming from a natural human activity to a regulated competitive sport?", ["The introduction of FINA as the global governing body", "The construction of artificial public swimming pools", "The inclusion of women in the Olympic Games", "The invention of the butterfly stroke"], 1),
    ("In terms of institutional evolution, which of the following events directly strengthened the international governance of swimming?", ["The creation of the National Swimming Society in 1837", "The introduction of swimming in the 1896 Olympics", "The formation of FINA in 1908", "The recognition of women’s swimming in 1912"], 2),
    ("Which of the following accurately demonstrates how rule enforcement led to innovation in Olympic swimming?", ["The banning of arm-over-head motion in breaststroke led to the birth of the butterfly stroke.", "The prohibition of women’s events led to freestyle dominance.", "The removal of backstroke from competition led to synchronized swimming.", "The limitation of pool length led to the creation of underwater swimming."], 0),
    ("Why was the inclusion of women’s swimming in the 1912 Stockholm Olympics a pivotal moment in the sport’s development?", ["It equalized the number of swimming events for both genders immediately.", "It marked the first time women competed under FINA’s governance.", "It solidified swimming’s place as a universal sport for both genders, influencing its global popularity.", "It introduced butterfly stroke and synchronized events for women."], 2),
    ("Which of the following best demonstrates the modern legacy of swimming’s Olympic evolution?", ["Only freestyle and breaststroke remain official strokes today.", "Olympic swimming now requires 25m pools for competition.", "Both men and women now compete in 17 events each in 50m Olympic pools.", "FINA no longer regulates swimming competitions."], 2),
    ("When was swimming first included in the Olympic Games?", ["1896", "1904", "1912", "1956"], 0),
    ("When was the butterfly stroke officially recognized in the Olympics?", ["1940", "1956", "1960", "1972"], 1),
    ("Who was the first man to swim across the English Channel using the breaststroke?", ["John Trudgen", "Captain Mathew Webb", "Michael Phelps", "Bongbong Marcos"], 1),
    ("Which stroke combines movements of the sidestroke and freestyle?", ["Dog Paddle", "Butterfly", "Trudgen", "Backstroke"], 2),
    ("Which of the following best explains why the freestyle or front crawl is considered the fastest swimming stroke?", ["It allows synchronized arm recovery above water, reducing resistance.", "The alternate arm motion and continuous flutter kick minimize drag and maximize propulsion.", "It uses symmetrical arm movement that increases forward thrust.", "The swimmer maintains a vertical body position to enhance breathing efficiency."], 1),
    ("The butterfly stroke originated from the breaststroke when swimmers discovered a faster arm motion. What rule change led to its official recognition in 1956?", ["The over-the-water arm recovery was banned in breaststroke, creating a new category.", "The dolphin kick was made illegal, forcing a new technique.", "FINA standardized freestyle to exclude symmetrical strokes.", "Backstroke replaced butterfly as an Olympic event."], 0),
    ("The sidestroke is unique because the swimmer’s head stays above water. What is the functional advantage of this position?", ["It is mainly used for competitive sprinting events.", "It increases forward speed and decreases drag.", "It allows the swimmer to perform underwater flips.", "It provides continuous breathing and is energy-efficient"], 3),
    ("Which stroke uses a scissors kick and evolved into the Trudgen stroke through alternating arm movements?", ["Sidestroke", "Butterfly", "Dog Paddle", "Backstroke"], 0),
    ("In terms of P.A.K. Method, which stroke demonstrates the highest physical demand due to simultaneous arm recovery and continuous undulating motion?", ["Freestyle", "Breaststroke", "Butterfly", "Trudgen"], 2),
    ("Anna joins her first swimming contest. She chooses the fastest stroke so she can reach the finish line quickly. Which stroke should she use?", ["Breaststroke", "Freestyle", "Sidestroke", "Dog Paddle"], 1),
    ("Liza watches Olympic swimmers moving their arms together in a wave-like motion while kicking like a dolphin. Which stroke are they performing?", ["Backstroke", "Butterfly", "Freestyle", "Trudgen"], 1),
    ("Carla enjoys swimming slowly while keeping her head above water. She paddles her arms in a circular motion under the surface. Which stroke is she using?", ["Dog Paddle", "Butterfly", "Backstroke", "Trudgen"], 0),
    ("Mia swims using a mix of sidestroke and freestyle movements — alternating her arms above the water but still using the scissors kick. What stroke is this?", ["Trudgen", "Butterfly", "Breaststroke", "Dog Paddle"], 0),
    ("Carla joins a freestyle relay, but her coach warns her not to use backstroke or butterfly. Which rule is her coach emphasizing?", ["Freestyle relay allows any stroke.", "Freestyle relay prohibits backstroke, breaststroke, and butterfly.", "Freestyle relay must begin with backstroke.", "Freestyle relay uses all four strokes."], 1),
    ("Julia participates in an individual medley event. Which stroke should she start with?", ["Backstroke", "Freestyle", "Butterfly", "Breaststroke"], 2),
    ("Coach Lara is arranging swimmers for a final race and places the fastest swimmer in the middle lane. What swimming rule is she following?", ["Seeding arrangement", "Floating technique", "Breathing pattern", "Stroke coordination"], 0),
    ("Miguel joined a sport where players paddle a narrow boat using a double-bladed paddle. What aquatic event is this?", ["Canoeing", "Kayaking", "Dragon Boat", "Water Polo"], 1),
    ("A team of 20 paddlers, a drummer, and a steerer works together in a boat race. Which event are they participating in?", ["Canoeing", "Kayaking", "Dragon Boat", "Water Polo"], 2),
    ("Seeding is a process by which a swimmer is assigned a certain lane and heat in an event. Competitors in each heat are assigned to lanes based on their seedtime. If there were 10 lanes, what lane does the fastest swimmer be placed?", ["Lane 3", "Lane 5", "Lane 6", "Lane 4"], 1),
    ("Coach Rivera is assigning the swimming order for a medley relay. Which arrangement shows the correct order of strokes?", ["Backstroke → Breaststroke → Butterfly → Freestyle", "Butterfly → Backstroke → Breaststroke → Freestyle", "Backstroke → Butterfly → Breaststroke → Freestyle", "Freestyle → Backstroke → Breaststroke → Butterfly"], 0),

    # --- Section 2 (Q51 to Q100) ---
    ("A swimmer competes in an Individual Medley event. He begins with backstroke and ends with freestyle. Which mistake has he made?", ["Wrong start and finish sequence.", "He used freestyle instead of butterfly.", "He skipped the breaststroke.", "No mistake; that is the correct order."], 0),
    ("In a freestyle relay, one swimmer chooses to perform breaststroke. What will happen?", ["Nothing; any stroke is allowed.", "The swimmer will be disqualified because breaststroke is not allowed.", "Only the lap time will not be counted.", "The relay will continue but lose points."], 1),
    ("In a dragon boat race, a crew member at the bow beats the drum out of rhythm. What will most likely happen?", ["The paddlers will follow the same rhythm.", "The boat will lose coordination and slow down.", "The steerer will take over the rhythm.", "The drummer will be replaced mid-race."], 1),
    ("In a swimming competition, the fastest swimmer is always placed in the middle lane. What is the reason for this arrangement?", ["The middle lane has the calmest water.", "It makes judging easier for referees.", "It helps balance the pool’s waves.", "It follows the tradition of lane seeding for visibility."], 0),
    ("A beginner struggles to stay afloat and panics during swim class. According to basic swimming instruction, what should the teacher emphasize first?", ["Mastering the freestyle stroke", "Learning to float and control breathing", "Practicing dolphin kicks", "Increasing speed underwater"], 1),
    ("The term “Taekwondo” comes from three Korean words. What does “Tae” mean?", ["Fist", "Kick", "Way", "Defense"], 1),
    ("Taekwondo originated from which country?", ["China", "Korea", "Japan", "Thailand"], 1),
    ("Each Taekwondo round lasts for how long?", ["1 minute", "2 minutes", "3 minutes", "5 minutes"], 1),
    ("How many points are given for a valid kick to the head in Olympic Taekwondo scoring?", ["2 points", "3 points", "4 points", "5 points"], 1),
    ("What score is given for a valid turning kick to the trunk protector?", ["2 points", "3 points", "4 points", "5 points"], 2),
    ("During a match, Player A performs a turning kick to the head of Player B. The kick is clean and valid. How many points should Player A receive?", ["3 points", "4 points", "5 points", "6 points"], 2),
    ("In the second round, the referee calls out “Cha-ryeot” and “Kyeong-rye.” What are the players expected to do?", ["Begin the fight", "Take their fighting stance", "Bow and show respect to each other", "Stop the fight and rest"], 2),
    ("In a medal round, Player A wins the first two rounds by small margins, while Player B dominates the third round. Who wins the match?", ["Player A, because they won more rounds", "Player B, because they scored more total points", "Both players tie", "The referee decides randomly"], 0),
    ("Which of the following is NOT a basic Taekwondo skill?", ["Kicking", "Blocking", "Standing", "Hand striking"], 2),
    ("A fighter performs a turning kick, but the opponent partially blocks it and contact is weak. What should the referee do?", ["Award 4 points for effort", "Award 2 points for a trunk kick", "No points, since it was not a valid impact", "Give a penalty for poor technique"], 2),
    ("A player performs two consecutive turning kicks to the head, both valid and clean. What is the total point score from those kicks?", ["6 points", "8 points", "9 points", "10 points"], 3),
    ("Player A lands a valid turning kick to the head, scoring 5 points, but immediately steps outside the boundary afterward. As a referee, how should the points and penalty be applied?", ["Cancel the points because of stepping out.", "Award the 5 points, then give a “gam-jeom” penalty for stepping out.", "Give only 2 points since the kick was not stable.", "Award no points and restart the match."], 1),
    ("A fighter leads in score but keeps avoiding combat in the last 20 seconds by running around the mat. What should the referee do?", ["Let the player continue since they are ahead.", "Issue a “gam-jeom” penalty for evasion.", "Restart the match from the center.", "Stop the match and reduce points."], 1),
    ("In a gold medal match, both athletes finish with the same score and same number of penalties. What rule determines the winner?", ["Referee decides by observation.", "A “Golden Point” round is conducted.", "The player who scored first wins.", "Judges vote for sportsmanship."], 1),
    ("Player A accidentally hits Player B below the belt. Player B cannot continue. The referee confirms it was unintentional. What should happen next?", ["Player A is disqualified immediately.", "The match resumes after Player B recovers.", "Player B loses the match for not continuing.", "Player A receives a “gam-jeom” for a low blow."], 3),
    ("During your P.E. class, your teacher asks you to demonstrate Sinawali. Which of the following correctly shows what you should do?", ["Perform solo defensive stances using one stick only.", "Demonstrate crisscross striking movements using two sticks of equal length.", "Perform freestyle moves with no pattern or partner.", "Show blocking and punching combinations using your bare hands."], 1),
    ("You are assigned to join the Full Contact Event in Arnis. Which of the following should you expect during the competition?", ["A choreographed demonstration of artistic movements.", "A one-round performance judged for creativity.", "A three-round fight using padded sticks and protective gear.", "A solo exhibition of defensive forms."], 2),
    ("In a Full Contact Arnis match, your opponent disarmed you twice in a round. What will most likely happen next?", ["The round continues until time runs out.", "The opponent automatically wins the round.", "Both players restart from their corners.", "The match is stopped, and the judges deduct points."], 1),
    ("During an Arnis training, you observe two students performing rhythmic strikes with both hands in a weaving pattern. What Arnis style are they demonstrating?", ["Anyo", "Disarming", "Sinawali", "Counterattack"], 2),
    ("If an Arnis stick has 28 inches in length, how many nodes would you expect it to have?", ["One node", "Two nodes", "Three or four nodes", "Five nodes"], 2),
    ("According to Republic Act No. 9850, Arnis holds what official recognition in the Philippines?", ["The national dance", "The national self-defense technique", "The national martial art and sport", "The national heritage performance"], 2),
    ("During a Full Contact Arnis match, Player A gains five points ahead in the second round. What should the referee do according to the rules?", ["Continue the round until the time runs out.", "Stop the round and declare Player A the winner of the bout.", "Pause the match for confirmation from judges.", "Let the third round decide the final result."], 1),
    ("An Arnis athlete performed a routine lasting for 1 minute and 30 seconds with smooth execution and powerful strikes but lacked coordination. In which event would this performance be evaluated?", ["Sinawali Training", "Anyo Event", "Full Contact Match", "Disarming Routine"], 1),
    ("You are one of the judges in an Anyo competition. One performer shows great speed but performs only 45 seconds. What should your decision be?", ["Give high points for speed.", "Deduct points for not meeting the time requirement.", "Disqualify the performer immediately.", "Ask the performer to repeat the routine."], 1),
    ("During a P.E. demonstration, two students are asked to show Sinawali, but one student uses a longer stick than the other. What principle of Arnis training is violated?", ["Proper posture and stance", "Equality of weapon length for balance and rhythm", "Mastery of defensive blocks", "Safety during performance"], 1),
    ("A player in a Full Contact match disarmed his opponent once and then gained three clean strikes to the trunk. What must happen next?", ["The player automatically wins the round.", "The referee awards points but continues the match.", "The referee stops the match due to disarming.", "The judges decide through majority scoring."], 1),
    ("You are officiating an Anyo competition. A participant exceeds the 2-minute limit but performs exceptional techniques. What should be done according to competition rules?", ["Allow a bonus score for excellent technique.", "Apply a time penalty deduction.", "Disqualify the participant.", "Let the head judge decide through special scoring."], 1),
    ("A coach instructs players to emphasize power strikes rather than rhythm during a Sinawali drill. What training focus is being prioritized?", ["Coordination and teamwork", "Strength and striking accuracy", "Endurance and timing", "Speed and flexibility"], 1),
    ("In a Full Contact Event, the surface becomes slippery due to water, and a player slips. What should the referee do?", ["Count it as a foul against the player.", "Stop the match temporarily for safety.", "Let the match continue to test balance.", "Award points to the standing player."], 1),
    ("What is the standard size of the playing area in a Full Contact Arnis event?", ["5 x 5 meters", "6 x 6 meters", "8 x 8 meters", "10 x 10 meters"], 2),
    ("What does the term Sepak Takraw mean?", ["To kick a ball", "To hit with hands", "To throw and catch", "To strike with a racket"], 0),
    ("Which body part is not used in playing Sepak Takraw?", ["Head", "Chest", "Feet", "Hands"], 3),
    ("What is the main objective of Sepak Takraw?", ["To hit the net with the ball", "To make the opponents commit a fault", "To kick the ball longer than the other team", "To strike the ball using hands"], 1),
    ("What is the main duty of the Feeder in Sepak Takraw?", ["To spike and block", "To serve the ball", "To toss or set the ball for the Killer", "To catch and throw the ball"], 2),
    ("How many points must a team score to win a set?", ["15 points", "18 points", "21 points", "25 points"], 2),
    ("The Feeder sets the ball too close to the net, allowing the Killer to spike but the ball touches the net and drops on their side. What should the team have done differently?", ["The Feeder should have tossed higher and away from the net", "The Tekong should have moved forward", "The Killer should have spiked softer", "The team should have changed positions and changed game strategy immediately"], 0),
    ("A Killer performs a strong spike that lands inside the opponent’s court, but the referee notices that the Killer’s foot touched the net. What happens next?", ["Point for the spiking team", "Replay", "Fault against the spiking team", "No fault; continue play"], 2),
    ("The score is 20–20 in the final set. The Tekong of Team A serves, but the serve hits the net and fails to cross. What is the referee's correct call?", ["Replay the rally because the score is tied.", "Award one point to Team A and allow another serve.", "Award one point to Team B because of a service fault.", "Declare a let and repeat the serve."], 2),
    ("During a serve, the Tekong accidentally misses the ball when trying to kick it. What happens next?", ["The serve is replayed", "The team loses a point", "The player can try again", "The referee gives a warning only"], 1),
    ("Team A wins the first set with 21 points. What should they do next to win the match?", ["Win one more set", "Win by at least 10 points", "Win three sets", "End the game immediately"], 0),
    ("The score is 20–20 in a set. What must a team do to win?", ["Be the first to score 22 points", "Win by 2 points or reach 25 points", "Score exactly 21 points", "Wait for the referee’s signal"], 1),
    ("During a rally, the ball hits the net but still crosses to the opponent’s side. What should happen?", ["The ball is still in play", "The rally ends", "The server repeats the serve", "The referee calls a fault"], 0),
    ("The Tekong of Team B serves the ball and it hits the net without crossing over. What is the call?", ["Replay", "Fault – point for Team A", "Let serve", "Warning"], 1),
    ("The Feeder sets the ball perfectly, and the Killer spikes it into the opponent’s court, earning a point. Who should receive most credit for this teamwork?", ["Tekong", "Feeder and Killer", "Feeder", "Killer"], 1),
    ("In Sepak Takraw, when a player strikes the ball over the net, what type of movement is being shown?", ["Leaping and Extension", "Jumping and Flexion", "Hopping and Spiking", "Galloping and Tossing"], 0),

    # --- Section 3 (Q101 to Q150) ---
    ("A basketball player consistently loses balance when landing after a rebound. Which adjustment will BEST improve stability?", ["Increase speed before jumping", "Narrow the landing stance", "Lower the center of gravity upon landing", "Keep the body upright and stiff"], 2),
    ("A volleyball coach notices that players get tired quickly during long rallies. Which training focus will MOST improve this problem?", ["Plyometric training", "Speed training", "Cardiovascular endurance training", "Maximum strength training"], 2),
    ("During a soccer match, a player keeps overshooting passes. Which biomechanical correction is MOST appropriate?", ["Increase kicking force", "Adjust angle and follow-through", "Kick only with the toe", "Reduce visual focus"], 1),
    ("A track athlete runs fast in the first 100m but fades in the last part of a 400m race. What conditioning is MOST needed?", ["Agility", "Muscular strength", "Anaerobic endurance", "Reaction time"], 2),
    ("In badminton, an opponent stays near the net. What is the BEST tactical response?", ["Drop shot", "Clear shot", "Net shot", "Weak return"], 1),
    ("A basketball player dribbles effectively but loses control under pressure. Which practice method BEST improves game performance?", ["Isolated dribbling drills", "Slow walking drills", "Game-simulated drills", "Static stretching"], 2),
    ("A sprinter wants to improve start explosiveness. Which training is MOST effective?", ["Long slow distance", "Static stretching", "Plyometric exercises", "Yoga"], 2),
    ("In volleyball defense, a player reacts late to spikes. Which ability should be developed?", ["Balance", "Reaction time", "Flexibility", "Coordination"], 1),
    ("A coach designs drills that mimic actual competition situations. Which training principle is applied?", ["Reversibility", "Individuality", "Specificity", "Overload"], 2),
    ("A tennis player always returns cross-court even when the opponent leaves the line open. What tactical error is being made?", ["Poor grip", "Lack of anticipation", "Inefficient swing", "Overtraining"], 1),
    ("A PE teacher increases training load weekly to avoid plateaus. Which principle is emphasized?", ["Specificity", "Progression", "Recovery", "Adaptation"], 1),
    ("In basketball, why is bending the knees before a jump shot important?", ["It reduces air resistance", "It stores elastic energy for force production", "It shortens shooting distance", "It prevents traveling"], 1),
    ("A soccer team presses high but concedes goals late in the game. What factor MOST likely causes this?", ["Poor tactics", "Weak technical skills", "Low aerobic capacity", "Bad officiating"], 2),
    ("In swimming, which change MOST reduces drag and improves speed?", ["Wider arm recovery", "Streamlined body position", "Faster kicking only", "Higher head position"], 1),
    ("A volleyball spiker lacks power despite good timing. Which physical quality should be prioritized?", ["Flexibility", "Muscular strength and power", "Balance", "Endurance"], 1),
    ("A basketball defender often gets beaten off the dribble. Which movement skill should be trained?", ["Linear speed", "Lateral agility", "Static balance", "Vertical jump"], 1),
    ("In badminton doubles, your opponents play mostly to the backcourt. Which formation adjustment is BEST?", ["Both players stay in front", "Side-by-side defense", "Front-and-back offense", "Random positioning"], 1),
    ("A track coach wants athletes to peak during competition season. Which planning strategy is MOST appropriate?", ["Constant high load", "No rest periods", "Periodization", "Random training"], 2),
    ("A basketball player shoots accurately in practice but poorly in games. What psychological factor is MOST involved?", ["Nutrition", "Game anxiety", "Flexibility", "Aerobic capacity"], 1),
    ("In soccer, quick one-touch passes are effective mainly because they:", ["Increase possession time", "Reduce opponent reaction time", "Slow the game", "Increase fatigue"], 1),
    ("A basketball player jumps high but lands stiffly and gets injured often. Which correction will BEST reduce injury risk?", ["Increase jump height", "Land with knees and hips flexed", "Keep legs straight", "Increase running speed"], 1),
    ("A volleyball team struggles against quick attacks. Which defensive training should be prioritized?", ["Strength training", "Reaction and anticipation drills", "Long-distance running", "Static stretching"], 1),
    ("In soccer, a winger beats defenders but fails to cross accurately. What element MOST needs improvement?", ["Speed", "Balance", "Technique and timing", "Endurance"], 2),
    ("A badminton player tires after repeated smashes. Which energy system is MOST stressed and should be trained?", ["ATP-PC system", "Aerobic system", "Anaerobic glycolytic system", "Flexibility system"], 2),
    ("A track athlete slows down in the final meters of a sprint. Which factor MOST limits performance?", ["Reaction time", "Speed endurance", "Flexibility", "Balance"], 1),
    ("In basketball, why is follow-through important in shooting?", ["It increases defense", "It controls direction and force", "It shortens release time", "It prevents fouls"], 1),
    ("A soccer goalkeeper reacts late to close-range shots. Which training will BEST help?", ["Long slow running", "Flexibility drills", "Reaction and perceptual training", "Strength lifting only"], 2),
    ("In volleyball, a blocker jumps too early. What tactical mistake is being committed?", ["Poor communication", "Incorrect timing and reading of the hitter", "Weak legs", "Bad positioning only"], 1),
    ("A coach wants players to transfer training gains directly into competition. What type of practice is MOST effective?", ["Repetitive isolated drills", "Game-like simulations", "Passive observation", "Stretching sessions"], 1),
    ("A tennis player always stays behind the baseline even when attacking. Which tactical weakness is shown?", ["Poor grip", "Lack of court positioning awareness", "Weak legs", "Overtraining"], 1),
    ("In swimming starts, why is a powerful leg drive critical?", ["To increase buoyancy", "To maximize horizontal velocity off the block", "To slow water entry", "To reduce breathing"], 1),
    ("A basketball defender keeps crossing feet and loses balance. Which movement correction is BEST?", ["Sprint forward", "Use lateral shuffle", "Jump often", "Stand upright"], 1),
    ("In soccer pressing, the main tactical purpose is to:", ["Slow your own team", "Reduce opponent time and space", "Increase ball possession only", "Save energy"], 1),
    ("A badminton doubles team keeps getting confused in defense. Which concept should be emphasized?", ["Individual skill", "Communication and positioning", "Speed only", "Power training"], 1),
    ("In basketball, why is core strength important for shooting and passing?", ["For decoration", "To transfer force efficiently through the kinetic chain", "To reduce height", "To limit motion"], 1),
    ("A track coach schedules heavy training every day without rest. What principle is being violated?", ["Specificity", "Overload", "Recovery", "Progression"], 2),
    ("A volleyball spiker hits hard but out of bounds often. Which adjustment will MOST help?", ["Add more power", "Improve approach angle and arm swing control", "Jump higher", "Ignore placement"], 1),
    ("In soccer, switching play is effective because it:", ["Makes the ball heavier", "Exploits space away from pressure", "Slows the attack", "Tires teammates"], 1),
    ("A basketball player loses shooting form late in the game. Which cause is MOST likely?", ["Lack of flexibility", "Poor officiating", "Muscular fatigue", "Weak eyesight"], 2),
    ("In badminton, deception shots are effective mainly because they:", ["Increase rally time", "Reduce opponent anticipation", "Increase your fatigue", "Improve grip"], 1),
    ("A swimmer lifts the head too high while breathing in freestyle, causing the hips to sink. Which correction is BEST?", ["Kick harder", "Turn the head sideways while maintaining body alignment", "Hold the breath longer", "Increase arm speed"], 1),
    ("During a race, a swimmer loses speed at the turn. Which element MOST affects efficient wall push-off?", ["Arm recovery", "Streamline position and leg drive", "Breathing pattern", "Stroke count"], 1),
    ("A beginner swimmer experiences early fatigue in a 200-meter event. Which training focus is MOST appropriate?", ["Maximum strength", "Aerobic endurance", "Reaction time", "Flexibility only"], 1),
    ("In butterfly stroke, timing errors between arms and kick reduce propulsion. What concept is MOST violated?", ["Buoyancy", "Coordination", "Balance", "Resistance"], 1),
    ("A swimmer’s hand enters the water crossing the midline, causing zigzag motion. What biomechanical problem occurs?", ["Increased propulsion", "Increased drag and loss of direction", "Higher buoyancy", "Faster recovery"], 1),
    ("Why is a streamlined body position important after a dive start?", ["To increase breathing", "To reduce drag and maintain velocity", "To slow the swimmer", "To improve floating"], 1),
    ("A backstroke swimmer’s hips drop during the race. Which adjustment BEST improves body position?", ["Hold breath longer", "Engage core and maintain steady kick", "Swing arms wider", "Shorten the stroke"], 1),
    ("A swimmer finishes strong in short races but fades in long-distance events. Which energy system MOST needs development?", ["ATP-PC", "Anaerobic", "Aerobic", "Flexibility"], 2),
    ("In breaststroke, why is a proper glide phase important?", ["It wastes time", "It maximizes efficiency between propulsion phases", "It increases drag", "It reduces oxygen use"], 1),
    ("A swimmer keeps slipping during flip turns. Which factor MOST contributes to this error?", ["Weak arms", "Poor wall contact and foot placement", "Long stroke length", "Slow breathing"], 1)
]

os.makedirs('lib/data/bped_spec_drill_4', exist_ok=True)

def generate_section(sec_id, start_idx, end_idx):
    sec_items = raw_items[start_idx:end_idx]
    code = f"import '../../models/question.dart';\n\n"
    code += f"const List<Question> bpedSpecDrill4Section{sec_id}Questions = [\n"
    
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
    
    file_path = f"lib/data/bped_spec_drill_4/bped_spec_drill_4_section_{sec_id}.dart"
    with open(file_path, "w") as f:
        f.write(code)
    print(f"Generated {file_path} with {len(sec_items)} items.")

generate_section(1, 0, 50)
generate_section(2, 50, 100)
generate_section(3, 100, 150)

print("All 3 BPED Drill 4 section files successfully generated!")
