import os
import json

raw_items = [
    # 1..50
    ("Football is a game played by two teams of how many players each?", ["9", "10", "11", "12"], 2),
    ("What body is responsible for governing international football competitions?", ["FIVB", "FIFA", "IOC", "AFC"], 1),
    ("The main goal of the defenders is to:", ["Pass the ball to the forwards", "Stop the opposing team from entering the goal area", "Kick the ball to the goalkeeper", "Create scoring opportunities"], 1),
    ("What is the role of a center forward in football?", ["To defend the goal", "To organize plays from the midfield", "To score goals or create scoring chances", "To guard the opposing striker"], 2),
    ("Which football position is also called a \"striker\"?", ["Goalkeeper", "Center forward", "Right winger", "Midfielder"], 1),
    ("What does a yellow card in football signify?", ["Dismissal from the match", "Warning or caution to a player", "Goal cancellation", "Free kick awarded"], 1),
    ("What happens when a player receives two yellow cards in the same match?", ["Awarded a free kick", "Receives a red card and is expelled", "Gets a warning only", "Substituted automatically"], 1),
    ("A red card in football means that:", ["The player is warned", "The player is suspended temporarily", "The player is dismissed and cannot be replaced", "The referee pauses the game"], 2),
    ("Which football player delivered the Philippines’ first-ever goal in the Women’s World Cup?", ["Hali Long", "Sarina Bolden", "Olivia McDaniel", "Katrina Guillou"], 1),
    ("The outside fullbacks in football usually:", ["Play near the goalkeeper", "Move constantly from side to side", "Stay on the left and right flanks to stop the ball", "Lead offensive attacks"], 2),
    ("The captain winning the coin toss chooses:", ["Whether to start first or not", "Which goalpost to attack first", "The type of ball used", "The referee’s side"], 1),
    ("Midfielders must be the fittest players because they:", ["Stay near the goal", "Run the most distance and connect plays", "Perform goal kicks", "Only assist defenders"], 1),
    ("The striker kicks the ball and it goes into the goal. What happens next?", ["The goal counts and play restarts with a kickoff", "The ball is returned to the same team", "The striker must repeat the kick", "The goal is canceled automatically"], 0),
    ("If the striker constantly gets caught offside, what adjustment should the coach make to improve goal-scoring chances?", ["Move the striker closer to the goal", "Encourage the striker to time runs better", "Tell the striker to defend more", "stay behind fullbacks before the pass"], 1),
    ("The goalkeeper is excellent at catching crosses but poor at distributing the ball. How could this weakness affect the team’s performance?", ["The team may lose scoring chances due to slow counterattacks", "The goalkeeper will concede more goals", "Defenders will commit more fouls", "The referee will issue more yellow cards"], 0),
    ("The main objective of basketball is to:", ["Defend the basket at all times", "Shoot the ball into the opponent’s basket and score more points", "Shoot the ball into their own basket and score more points", "Bounce the ball until the timer ends without any violations"], 1),
    ("In basketball, how many players are allowed on the court for each team during play?", ["5", "10", "12", "24"], 0),
    ("What is the term for bouncing the ball while moving?", ["Passing", "Dribbling", "Shooting", "Rebounding"], 1),
    ("A free throw in basketball is worth how many points?", ["1 point", "2 points", "3 points", "Depends on referee"], 0),
    ("The tall player who plays near the basket to rebound and block shots is called:", ["Guard", "Center", "Forward", "Shooter"], 1),
    ("The most common defensive system where each player guards one opponent is:", ["Zone defense", "Man-to-man defense", "Press defense", "Full-court trap"], 1),
    ("The ball accidentally goes out of bounds after touching a player’s hand. What will happen next?", ["The same player continues to play", "The other team gets the ball for a throw-in", "A jump ball occurs", "The referee restarts the game"], 1),
    ("A player shoots the ball beyond the three-point arc and scores. How many points are awarded?", ["One", "Two", "Three", "Four"], 2),
    ("During a free throw, the player scores the basket. What should the referee do?", ["Award one point and continue play", "Allow another free throw", "Cancel the shot", "Award three points"], 0),
    ("During the tip-off, the referee throws the ball up between two players. What are the other players supposed to do?", ["Stand still until the ball is tapped", "Jump with the referee", "Leave the court", "Dribble the ball"], 0),
    ("A team keeps missing shots because the defenders block most attempts near the ring. What strategy could best improve their offense?", ["Attempt more three-point shots to stretch the defense", "Pass the ball less to speed up play", "Substitute all tall players", "Focus only on free throws"], 0),
    ("The point guard notices the opponent’s defense is using full-court pressure. What should he do to help his team advance the ball effectively?", ["Dribble past the defenders alone", "Call a timeout and plan a passing strategy", "Shoot from the backcourt", "Wait for the shot clock to expire"], 1),
    ("If a player keeps committing fouls due to poor defensive timing, what training focus is most suitable?", ["Improve agility and body control", "Increase upper body strength", "Practice long-range shooting", "Learn offensive screens"], 0),
    ("If a team has excellent defense but poor shooting, what area should they focus on to win more games?", ["Rebounding", "Passing", "Shooting accuracy", "Foul drawing"], 2),
    ("In official FIBA play, the height of the basketball ring from the floor is:", ["9 feet", "10 feet", "11 feet", "12 feet"], 1),
    ("Volleyball was invented by William G. Morgan in what year?", ["1875", "1895", "1905", "1910"], 1),
    ("Volleyball was originally called:", ["Handball", "Netball", "Mintonette", "Spikeball"], 2),
    ("How many players are on each volleyball team during play?", ["5", "6", "7", "8"], 1),
    ("The maximum number of times a team may hit the ball before sending it over the net is:", ["2", "3", "4", "Unlimited"], 1),
    ("A player may not hit the ball twice in succession unless:", ["The ball touches the net", "It is during a block", "The referee allows it", "It is during a spike"], 1),
    ("The first team to reach how many points (with at least 2-point lead) wins a standard set?", ["21", "23", "25", "30"], 2),
    ("What is the main purpose of the serve in volleyball?", ["To set the ball for a teammate", "To put the ball into play", "To defend the court", "To confuse the opponents"], 1),
    ("The skill used to position the ball for a teammate’s attack is:", ["Pass", "Serve", "Set", "Block"], 2),
    ("The most powerful offensive move, hitting the ball downward into the opponent’s court, is called a:", ["Spike", "Dig", "Toss", "Bump"], 0),
    ("The rotation system in volleyball moves players:", ["Clockwise", "Counterclockwise", "Randomly", "By coach’s decision only"], 0),
    ("Volleyball became an official Olympic sport in:", ["1948", "1956", "1964", "1972"], 2),
    ("The serving player hits the ball and it lands directly on the opponent’s court untouched. What is this called?", ["Spike", "Ace", "Fault", "Dig"], 1),
    ("The ball touches the net during a serve but still goes over and lands inside the opponent’s court. What happens?", ["The serve counts and play continues", "The serve is repeated", "The server loses the point", "The referee gives a warning"], 0),
    ("A team often loses points because their spiker hits the ball out of bounds. Which skill should the coach prioritize during training?", ["Serve accuracy", "Ball control and timing during the spike", "Blocking form", "Digging and floor defense"], 1),
    ("In a crucial rally, the back-row player jumps and spikes the ball in front of the attack line. What should the referee decide?", ["Legal play, continue rally", "Fault—back-row attack violation", "Replay the point", "Award a time-out"], 1),
    ("A pitcher keeps throwing high balls, missing the strike zone. Which adjustment would most likely help him improve accuracy?", ["Decrease pitching speed and adjust release point", "Move closer to the batter", "Swing the bat slower", "Change gloves"], 0),
    ("During a close game, a batter decides to bunt instead of swing. Why might this be a strategic decision?", ["To hit a home run", "To advance a base runner safely", "To waste time", "To get a strikeout intentionally"], 1),
    ("The team’s outfielders are catching fewer fly balls. What is the most likely reason?", ["Poor communication and misjudged ball trajectory", "Too much focus on batting", "Weak throwing arm", "Small field dimensions"], 0),
    ("The batter hits the ball and runs to first base before the fielders catch it. What should the batter do?", ["Stop running", "Continue running to second base", "Stay safely on first base", "Leave the field"], 2),
    ("The pitcher throws a ball and it passes outside the strike zone without the batter swinging. What should the umpire call?", ["Strike", "Ball", "Out", "Hit"], 1),

    # 51..100
    ("The batter hits a high fly ball and a fielder catches it before it touches the ground. What happens?", ["The batter is out", "The batter scores a run", "The batter continues running", "The umpire ignores it"], 0),
    ("There are already three outs in the inning. What happens next?", ["The same team continues to bat", "The teams switch sides", "The inning restarts", "The game ends automatically"], 1),
    ("Baseball is a bat-and-ball game played between how many players on each team?", ["7", "8", "9", "10"], 2),
    ("The team on defense tries to:", ["Score more runs", "Strike out or put out runners", "Help batters get to base", "Hit the ball farther"], 1),
    ("The game of baseball originated in which country?", ["England", "Japan", "United States", "Canada"], 2),
    ("How many balls result in a “walk” (batter advances to first base)?", ["3", "4", "5", "6"], 1),
    ("The “inning” in baseball refers to:", ["One player’s turn at bat", "A period in which both teams bat once", "The warm-up phase", "The referee’s decision"], 1),
    ("A standard baseball game has how many innings?", ["6", "7", "8", "9"], 3),
    ("The “shortstop” position is located between which two bases?", ["First and second", "Second and third", "Third and home", "Pitcher and catcher"], 1),
    ("When a batter swings and misses the ball, it is called a:", ["Foul", "Ball", "Strike", "Out"], 2),
    ("The main objective of softball is to:", ["Prevent the pitcher from scoring", "Hit the ball and score runs by reaching home plate", "Catch as many balls as possible", "Avoid fouls and penalties"], 1),
    ("The shape of a softball field is similar to a:", ["Rectangle", "Circle", "Diamond", "Triangle"], 2),
    ("When a player hits the ball and reaches all four bases, it is called a:", ["Home run", "Double play", "Grand slam", "Fastball"], 0),
    ("A strike is called when the batter:", ["Hits the ball foul", "Swings and misses, or does not swing at a good pitch", "Is hit by the ball", "Runs off the base"], 1),
    ("A ball is called when:", ["The pitcher throws outside the strike zone and the batter doesn’t swing", "The batter hits the ball", "The fielder drops the ball", "The runner steps off base"], 0),
    ("The defensive team must make how many outs before switching sides?", ["2", "3", "4", "5"], 1),
    ("The pitcher throws underhand, and the batter hits the ball fair. What should the batter do?", ["Drop the bat and run to first base", "Stay in the box", "Wait for a call", "Walk away"], 0),
    ("The batter swings and misses three pitches. What happens?", ["Walk", "Strikeout", "Ball", "Replay"], 1),
    ("The batter bunts and the ball rolls in fair territory. What must she do?", ["Stay still", "Run to first base", "Pick up the ball", "Ask for time"], 1),
    ("The pitcher throws four balls outside the strike zone. What happens?", ["Strikeout", "Walk", "Replay", "Foul"], 1),
    ("The catcher catches a foul tip on the third strike. What happens?", ["Out", "Replay", "Safe", "Strike only"], 0),
    ("The batter swings and misses the ball three times. What is the decision?", ["Walk", "Out (Strikeout)", "Home run", "Ball"], 1),
    ("Which skill is used to throw the ball to another player accurately?", ["Pitching", "Catching", "Throwing", "Batting"], 2),
    ("What is the correct grip when holding a softball bat?", ["One hand only", "Two hands together on the handle", "One hand on top, one hand on bottom", "Hands apart"], 1),
    ("What skill is most important for fielders to prevent runs?", ["Hitting", "Catching and throwing", "Running", "Pitching"], 1),
    ("What is the main objective of badminton?", ["To hit the shuttlecock as hard as possible", "To make the shuttlecock land in the opponent’s half of the court", "To hit the shuttlecock below the net", "To keep the shuttlecock in the air for a long time"], 1),
    ("The game “Badminton” was originally called ______ in India.", ["Shuttle game", "Poona", "Racket sport", "Battledore"], 1),
    ("During a match, Ana’s score is 10, and she is about to serve. From which side of the court should she serve?", ["Left side", "Right side", "Any side", "Center of the court"], 1),
    ("The shuttlecock touched Ana’s shirt before she hit it. What should the umpire call?", ["Let", "Fault", "Replay", "Point for Ana"], 1),
    ("Ben hits the shuttle, and it lands exactly on the boundary line of his opponent’s court. What happens?", ["Out of bounds", "Replay", "Point for Ben", "Let serve"], 2),
    ("Mia won the first game of the match. What happens next?", ["The opponent serves first in the next game", "Mia serves first in the next game", "Both start a toss again", "The umpire decides"], 1),
    ("A rally continues until the shuttlecock...", ["Touches the net", "Touches the ground", "Passes twice over the net", "Bounces once on the floor"], 1),
    ("During service, the shuttle is hit above the server’s waist. What happens?", ["Legal serve", "Let", "Fault", "Point for the server"], 2),
    ("The score reaches 29-all. What will determine the winner of the game?", ["Whoever scores next point", "Whoever gets two-point lead", "Whoever served first", "Replay"], 0),
    ("If a player uses the backhand grip, where does the thumb usually rest?", ["On the round side of the handle", "Flat against the back of the handle", "Alongside the strings", "Between two fingers"], 1),
    ("Which grip is used to hit the shuttle on the non-dominant side of the body?", ["Forehand grip", "Backhand grip", "Reverse grip", "Power grip"], 1),
    ("In badminton, the side that wins a game shall ______.", ["Receive first in the next game", "Serve first in the next game", "Choose side of the court", "Rest for two minutes"], 1),
    ("During a rally, Player A accidentally touches the net with their racket while returning the shuttle, but the shuttle lands successfully inside Player B’s court. What should be the decision?", ["Point for Player A because the shuttle landed in", "Replay the rally", "Fault on Player A for touching the net", "Let since no player was injured"], 2),
    ("A right-handed player uses a backhand grip to return a shuttle on their dominant side. What might this cause?", ["A stronger and faster return", "A weaker and less controlled shot", "A better angle and balance", "No effect on the performance"], 1),
    ("If a player serves from the left side when the score is even, what kind of mistake has been made?", ["Service fault due to wrong side", "Service fault due to height", "It’s a let and should be replayed", "No fault, play continues"], 0),
    ("Table Tennis became an Olympic sport in what year?", ["1972", "1980", "1988", "1992"], 2),
    ("The head of the racket faces downward in which grip?", ["Forehand grip", "Pen-hold grip", "Cross grip", "Reverse grip"], 1),
    ("A rally with no score result is called a ______.", ["Point", "Let", "Serve", "Net shot"], 1),
    ("How many serves does each player get before switching?", ["1", "2", "3", "4"], 1),
    ("In doubles, after the receiver returns the serve, who should return next?", ["The same receiver", "Partner of the server", "Partner of the receiver", "Any player"], 1),
    ("Before service, the ball must be placed on...", ["The racket", "The table", "The open palm", "Any surface"], 2),
    ("In singles, who serves first is decided by...", ["The umpire", "Coin toss or lot", "Crowd decision", "Both players’ choice"], 1),
    ("If both players reach 10 points, and one player leads by one point but loses the next, what happens next?", ["Game ends immediately", "Game continues until one leads by two points", "Both players lose the set", "Service switches permanently"], 1),
    ("In doubles, if the partner of the server accidentally hits the ball before the receiver returns it, what should the umpire do?", ["Award point to server", "Call a let", "Award point to receiver", "Replay the rally"], 2),
    ("A player serves and the ball bounces twice on the receiver’s side before being hit. What is the outcome?", ["Point for the server", "Point for the receiver", "Let – replay the rally", "Fault serve"], 0),

    # 101..150
    ("During a doubles match, the server accidentally serves to the wrong half of the receiver’s court. What is the decision?", ["Point for receiver", "Let – replay the serve", "Fault serve", "No penalty; play continues"], 2),
    ("If a player’s shot hits the edge of the table and bounces up, what should happen?", ["Point for opponent", "Let – replay the rally", "Ball is in, rally continues", "Shot is invalid"], 2),
    ("During a rally, the ball hits the net, touches the opponent’s hand above the table, and falls back onto the striker’s side. What’s the decision?", ["Let", "Point for striker", "Point for receiver", "Replay serve"], 1),
    ("In doubles, Player A serves. The receiver returns the ball straight to Player A instead of Player B. What’s the ruling?", ["Point for serving team", "Let", "Replay", "Continue rally"], 0),
    ("During a rally, the ball hits the ceiling after bouncing on the opponent’s side. What is the call?", ["Point for striker", "Point for opponent", "Let", "Replay serve"], 0),
    ("During play, the ball lands on the baseline. What should the umpire call?", ["Out", "Let", "In", "Replay"], 2),
    ("A player wins six games while the opponent has four. What’s the result?", ["Game over", "Player wins the set", "Deuce set", "Tie-break"], 1),
    ("The player wins the first two sets in a best-of-three match. What happens?", ["Continue playing", "Match ends", "Start new game", "Tie-break round"], 1),
    ("What type of shot is used when the player hits before the ball bounces?", ["Volley", "Drop shot", "Smash", "Lob"], 0),
    ("The ITF was founded in what year?", ["1913", "1920", "1934", "1900"], 0),
    ("A shot that starts every point in tennis is called ______.", ["Volley", "Serve", "Smash", "Lob"], 1),
    ("A ball that travels high and deep into the opponent’s court is a ______.", ["Smash", "Drop shot", "Lob", "Serve"], 2),
    ("In tennis scoring, the sequence goes from Love → 15 → 30 → ______.", ["35", "40", "45", "Game"], 1),
    ("A powerful overhead shot done above the head is called ______.", ["Drop shot", "Smash", "Volley", "Lob"], 1),
    ("Which stroke lands softly just over the net?", ["Smash", "Drop shot", "Lob", "Volley"], 1),
    ("During a rally, a player volleys the ball before it crosses the net. What is the decision?", ["Legal return", "Fault", "Replay", "Point to that player"], 1),
    ("A tennis player performs a drop shot after several deep baseline rallies to catch the opponent off guard. What strategy does this demonstrate?", ["Defensive play", "Tactical variation to break rhythm", "Rule violation", "Poor shot selection"], 1),
    ("A player repeatedly uses drop shots when the opponent stays far behind the baseline. This shows ______.", ["Poor sportsmanship", "Strategic awareness of opponent’s position", "Defensive shot selection", "Violation of court rules"], 1),
    ("A player serves; the ball clips the receiver’s clothing before landing out. What is the call?", ["Fault", "Let", "Point for server", "Replay"], 2),
    ("A ball lands on the baseline, and a puff of chalk is seen. The opponent challenges it. What should Hawk-Eye confirm?", ["Out – because chalk puff means ball hit outside", "In – chalk indicates line contact", "Let", "Replay point"], 1),
    ("It is the essential part of a successful throw as it ensures that the athletes is in full control of the movement.", ["Coordination", "Power", "Pivot", "Balance"], 3),
    ("Which of the following statements shows the correct distinction between Artistic Expression and Cultural Literacy?", ["Artistic Expression refers to symbolic representation...", "Artistic Expression refers to continuous rebirth...", "Cultural Literacy refers to people's way of creatively...", "Cultural literacy refers to the students' pride in and active enjoyment of their own culture, whereas artistic expression refers to people's creative means of expressing their values, hopes, and concerns."], 3),
    ("Asian Music and Arts were taught in what Grade Level?", ["Grade 7", "Grade 8", "Grade 9", "Grade 10"], 1),
    ("Invented in England in the early days of the 20th century, the game table tennis was originally known as ________.", ["Whiff-whaff", "Gossima", "Ping pong", "All of the above"], 3),
    ("What is the number one racket game in China, Japan and the United States?", ["Table Tennis", "Pelota", "Lawn Tennis", "Badminton"], 0),
    ("An illegal play in badminton which result in loss of service is called:", ["A fight", "A fault", "A smash", "An ace"], 1),
    ("In which track event do teams of athlete run and pass on a baton to their team member?", ["Relay", "Hurdles", "Long Jump", "Pole Vault"], 0),
    ("A stroke frequently used by the right-handed player when returning a ball hit to his left, in which the paddle is held?", ["Backhand", "Forehand", "Backspin", "Topspin"], 0),
    ("How many feathers does the shuttlecock have?", ["15", "17", "18", "16"], 3),
    ("What is the eighth event in the 2nd day of decathlon?", ["Discus", "Pole Vault", "Javelin", "High Jump"], 1),
    ("What is the third event in the first day of the heptathlon?", ["100-meter hurdles", "Shot Put", "High Jump", "200 meters"], 1),
    ("In doubles event, when score is “love” the server serves from which service court?", ["Right to Right", "Left to Left", "Right to Left", "Left to Right"], 0),
    ("The word “Athletics” comes from the Greek word “Athlos,” which means ______.", ["Race", "Contest", "Speed", "Strength"], 1),
    ("Which of the following is a track event?", ["Discus throw", "High jump", "Sprint", "Pole vault"], 2),
    ("In hurdles, a runner knocks over a hurdle but continues and finishes the race. What’s the call?", ["Disqualification", "Legal run", "Penalty", "Replay"], 1),
    ("A 4x100 relay runner passes baton outside the exchange zone. What’s the result?", ["Legal pass", "Disqualification", "Warning", "Replay"], 1),
    ("During high jump, the bar falls off the stand after the jump. What’s the ruling?", ["Foul jump", "Successful jump", "Replay jump", "Cancel attempt"], 0),
    ("The 100-meter dash belongs to which category?", ["Long distance", "Middle distance", "Sprint or short distance", "Relay"], 2),
    ("Which throwing event uses a platelike implement?", ["Shot put", "Discus throw", "Hammer throw", "Javelin throw"], 1),
    ("The hammer throw uses a heavy ball attached to ______.", ["A pole", "A wire", "A rope", "A string"], 1),
    ("In the decathlon, which event is done on the second day?", ["100 meters", "400 meters", "1500 meters", "Shot put"], 2),
    ("During the second day of Decathlon, Leo is preparing for Pole Vault. Which event comes immediately before it?", ["Discus Throw", "110m Hurdles", "Javelin Throw", "1500m Run"], 0),
    ("Why are sprinters required to stay in their assigned lanes while distance runners may not?", ["To maintain fairness in equal distances", "To increase the challenge", "To reduce crowding", "To save time for officials"], 0),
    ("Why are heptathlon and decathlon considered tests of complete athletic ability?", ["They involve only sprint events", "They measure strength, speed, endurance, and skill", "They have longer running distances", "They use special equipment"], 1),
    ("A male athlete just finished the Long Jump in a Decathlon. What is his next event?", ["400m Run", "Shot Put", "High Jump", "110m Hurdles"], 1),
    ("A coach tells his athlete to rest after finishing 400m because the next day starts with hurdles. What event will open Day 2 of the Decathlon?", ["110m Hurdles", "Javelin Throw", "Pole Vault", "Long Jump"], 0),
    ("During the first day of the Heptathlon, Ana just finished the Shot Put event. What event will she compete in next?", ["100m Hurdles", "High Jump", "200m Run", "Long Jump"], 2),
    ("Although physical activities in the primitive society were practical in nature, primitive men still had to participate in recreational activities. Which of the following provided children in the primitive society preparation for adult responsibilities?", ["Dancing", "Mimetic games", "Physical exercise", "Chanting"], 1),
    ("A strong Persian army meant a healthy and physically fit army. Persian physical education was ____.", ["Centered and confined to men", "Focused on swimming, wrestling and gymnastics", "The modality for disciplining the mind and body.", "Developing military skills, high moral standards, and patriotism."], 3),
    ("This Pan-Hellenic game was done every 2 years to honor the Greek God Poseidon.", ["Olympia Festival", "Pythia Festival", "Nemea Festival", "Isthmia Festival"], 3)
]

os.makedirs('lib/data/bped_spec_drill_3', exist_ok=True)

def generate_section(sec_id, start_idx, end_idx):
    sec_items = raw_items[start_idx:end_idx]
    code = f"import '../../models/question.dart';\n\n"
    code += f"const List<Question> bpedSpecDrill3Section{sec_id}Questions = [\n"
    
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
    
    file_path = f"lib/data/bped_spec_drill_3/bped_spec_drill_3_section_{sec_id}.dart"
    with open(file_path, "w") as f:
        f.write(code)
    print(f"Generated {file_path} with {len(sec_items)} items.")

generate_section(1, 0, 50)
generate_section(2, 50, 100)
generate_section(3, 100, 150)

print("All 3 section files successfully generated!")
