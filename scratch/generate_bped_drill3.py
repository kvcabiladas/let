import os
import json
import re

# Complete list of 150 verified questions, options, and correct answer index
q_list = [
    # --- Section 1 (Q1 to Q50) ---
    {
        "id": 1,
        "questionText": "Football is a game played by two teams of how many players each?",
        "options": ["9", "10", "11", "12"],
        "correctAnswerIndex": 2, # C. 11
        "explanation": "Standard association football (soccer) is played between two teams of 11 players each."
    },
    {
        "id": 2,
        "questionText": "What body is responsible for governing international football competitions?",
        "options": ["FIVB", "FIFA", "IOC", "AFC"],
        "correctAnswerIndex": 1, # B. FIFA
        "explanation": "FIFA (Fédération Internationale de Football Association) is the international governing body for association football."
    },
    {
        "id": 3,
        "questionText": "The main goal of the defenders is to:",
        "options": [
            "Pass the ball to the forwards",
            "Stop the opposing team from entering the goal area",
            "Kick the ball to the goalkeeper",
            "Create scoring opportunities"
        ],
        "correctAnswerIndex": 1, # B
        "explanation": "The primary objective of defenders in football is to prevent the opposing team from attacking and scoring goals."
    },
    {
        "id": 4,
        "questionText": "What is the role of a center forward in football?",
        "options": [
            "To defend the goal",
            "To organize plays from the midfield",
            "To score goals or create scoring chances",
            "To guard the opposing striker"
        ],
        "correctAnswerIndex": 2, # C
        "explanation": "Center forwards (strikers) play closest to the opponent's goal and are mainly responsible for scoring goals."
    },
    {
        "id": 5,
        "questionText": "Which football position is also called a \"striker\"?",
        "options": ["Goalkeeper", "Center forward", "Right winger", "Midfielder"],
        "correctAnswerIndex": 1, # B
        "explanation": "A center forward is commonly referred to as a striker."
    },
    {
        "id": 6,
        "questionText": "What does a yellow card in football signify?",
        "options": [
            "Dismissal from the match",
            "Warning or caution to a player",
            "Goal cancellation",
            "Free kick awarded"
        ],
        "correctAnswerIndex": 1, # B
        "explanation": "A yellow card is shown by the referee to indicate that a player has been officially cautioned."
    },
    {
        "id": 7,
        "questionText": "What happens when a player receives two yellow cards in the same match?",
        "options": [
            "Awarded a free kick",
            "Receives a red card and is expelled",
            "Gets a warning only",
            "Substituted automatically"
        ],
        "correctAnswerIndex": 1, # B
        "explanation": "Receiving two yellow cards in a single match results in an automatic red card and ejection."
    },
    {
        "id": 8,
        "questionText": "A red card in football means that:",
        "options": [
            "The player is warned",
            "The player is suspended temporarily",
            "The player is dismissed and cannot be replaced",
            "The referee pauses the game"
        ],
        "correctAnswerIndex": 2, # C
        "explanation": "A red card results in immediate ejection from the match, and the team must play with one fewer player."
    },
    {
        "id": 9,
        "questionText": "Which football player delivered the Philippines’ first-ever goal in the Women’s World Cup?",
        "options": ["Hali Long", "Sarina Bolden", "Olivia McDaniel", "Katrina Guillou"],
        "correctAnswerIndex": 1, # B. Sarina Bolden
        "explanation": "Sarina Bolden scored the historical first Women's World Cup goal for the Philippines against New Zealand in 2023."
    },
    {
        "id": 10,
        "questionText": "The outside fullbacks in football usually:",
        "options": [
            "Play near the goalkeeper",
            "Move constantly from side to side",
            "Stay on the left and right flanks to stop the ball",
            "Lead offensive attacks"
        ],
        "correctAnswerIndex": 2, # C
        "explanation": "Fullbacks defend the wide areas (left and right flanks) to prevent wingers from crossing or cutting inside."
    },
    {
        "id": 11,
        "questionText": "The captain winning the coin toss chooses:",
        "options": [
            "Whether to start first or not",
            "Which goalpost to attack first",
            "The type of ball used",
            "The referee’s side"
        ],
        "correctAnswerIndex": 1, # B
        "explanation": "Under IFAB laws, the team winning the toss decides either which goal to attack in the first half or to take the kickoff."
    },
    {
        "id": 12,
        "questionText": "Midfielders must be the fittest players because they:",
        "options": [
            "Stay near the goal",
            "Run the most distance and connect plays",
            "Perform goal kicks",
            "Only assist defenders"
        ],
        "correctAnswerIndex": 1, # B
        "explanation": "Midfielders link defense and offense, covering the most ground during a match."
    },
    {
        "id": 13,
        "questionText": "The striker kicks the ball and it goes into the goal. What happens next?",
        "options": [
            "The goal counts and play restarts with a kickoff",
            "The ball is returned to the same team",
            "The striker must repeat the kick",
            "The goal is canceled automatically"
        ],
        "correctAnswerIndex": 0, # A
        "explanation": "When a goal is scored, play restarts with a kickoff by the team that conceded the goal."
    },
    {
        "id": 14,
        "questionText": "If the striker constantly gets caught offside, what adjustment should the coach make to improve goal-scoring chances?",
        "options": [
            "Move the striker closer to the goal",
            "Encourage the striker to time runs better",
            "Tell the striker to defend more",
            "Stay behind fullbacks before the pass"
        ],
        "correctAnswerIndex": 1, # B
        "explanation": "Timing runs properly ensures the forward stays onside when the ball is played."
    },
    {
        "id": 15,
        "questionText": "The goalkeeper is excellent at catching crosses but poor at distributing the ball. How could this weakness affect the team’s performance?",
        "options": [
            "The team may lose scoring chances due to slow counterattacks",
            "The goalkeeper will concede more goals",
            "Defenders will commit more fouls",
            "The referee will issue more yellow cards"
        ],
        "correctAnswerIndex": 0, # A
        "explanation": "Poor goalkeeper distribution delays transition play and slows down fast-break counterattacks."
    },
    {
        "id": 16,
        "questionText": "The main objective of basketball is to:",
        "options": [
            "Defend the basket at all times",
            "Shoot the ball into the opponent’s basket and score more points",
            "Shoot the ball into their own basket and score more points",
            "Bounce the ball until the timer ends without any violations"
        ],
        "correctAnswerIndex": 1, # B
        "explanation": "The primary objective is to outscore the opponent by shooting the ball into the opponent's hoop."
    },
    {
        "id": 17,
        "questionText": "In basketball, how many players are allowed on the court for each team during play?",
        "options": ["5", "10", "12", "24"],
        "correctAnswerIndex": 0, # A. 5
        "explanation": "Basketball is played with 5 active players on the court per team."
    },
    {
        "id": 18,
        "questionText": "What is the term for bouncing the ball while moving?",
        "options": ["Passing", "Dribbling", "Shooting", "Rebounding"],
        "correctAnswerIndex": 1, # B. Dribbling
        "explanation": "Dribbling is the continuous bouncing of the ball against the floor while traveling."
    },
    {
        "id": 19,
        "questionText": "A free throw in basketball is worth how many points?",
        "options": ["1 point", "2 points", "3 points", "Depends on referee"],
        "correctAnswerIndex": 0, # A. 1 point
        "explanation": "Each unhindered free throw shot from behind the free-throw line counts as 1 point."
    },
    {
        "id": 20,
        "questionText": "The tall player who plays near the basket to rebound and block shots is called:",
        "options": ["Guard", "Center", "Forward", "Shooter"],
        "correctAnswerIndex": 1, # B. Center
        "explanation": "The center is typically the tallest player, positioned near the basket for rim protection and rebounding."
    },
    {
        "id": 21,
        "questionText": "The most common defensive system where each player guards one opponent is:",
        "options": ["Zone defense", "Man-to-man defense", "Press defense", "Full-court trap"],
        "correctAnswerIndex": 1, # B
        "explanation": "In man-to-man defense, each defensive player is assigned to guard a specific offensive opponent."
    },
    {
        "id": 22,
        "questionText": "The ball accidentally goes out of bounds after touching a player’s hand. What will happen next?",
        "options": [
            "The same player continues to play",
            "The other team gets the ball for a throw-in",
            "A jump ball occurs",
            "The referee restarts the game"
        ],
        "correctAnswerIndex": 1, # B
        "explanation": "Possession is awarded to the opposing team when the ball goes out of bounds after touching a player."
    },
    {
        "id": 23,
        "questionText": "A player shoots the ball beyond the three-point arc and scores. How many points are awarded?",
        "options": ["One", "Two", "Three", "Four"],
        "correctAnswerIndex": 2, # C. Three
        "explanation": "Successful field goals taken from beyond the 3-point line count for 3 points."
    },
    {
        "id": 24,
        "questionText": "During a free throw, the player scores the basket. What should the referee do?",
        "options": [
            "Award one point and continue play",
            "Allow another free throw",
            "Cancel the shot",
            "Award three points"
        ],
        "correctAnswerIndex": 0, # A
        "explanation": "A successful free throw awards 1 point and play proceeds according to the penalty state or inbounds restart."
    },
    {
        "id": 25,
        "questionText": "During the tip-off, the referee throws the ball up between two players. What are the other players supposed to do?",
        "options": [
            "Stand still until the ball is tapped",
            "Jump with the referee",
            "Leave the court",
            "Dribble the ball"
        ],
        "correctAnswerIndex": 0, # A
        "explanation": "Non-jumpers must remain stationary outside the center circle until the ball is legally tapped."
    },
    {
        "id": 26,
        "questionText": "A team keeps missing shots because the defenders block most attempts near the ring. What strategy could best improve their offense?",
        "options": [
            "Attempt more three-point shots to stretch the defense",
            "Pass the ball less to speed up play",
            "Substitute all tall players",
            "Focus only on free throws"
        ],
        "correctAnswerIndex": 0, # A
        "explanation": "Shooting effectively from perimeter/3-point range forces defenders out of the paint, creating space."
    },
    {
        "id": 27,
        "questionText": "The point guard notices the opponent’s defense is using full-court pressure. What should he do to help his team advance the ball effectively?",
        "options": [
            "Dribble past the defenders alone",
            "Call a timeout and plan a passing strategy",
            "Shoot from the backcourt",
            "Wait for the shot clock to expire"
        ],
        "correctAnswerIndex": 1, # B
        "explanation": "Calling a timeout allows the team to organize press-break passing alignments."
    },
    {
        "id": 28,
        "questionText": "If a player keeps committing fouls due to poor defensive timing, what training focus is most suitable?",
        "options": [
            "Improve agility and body control",
            "Increase upper body strength",
            "Practice long-range shooting",
            "Learn offensive screens"
        ],
        "correctAnswerIndex": 0, # A
        "explanation": "Agility and footwork control enable defenders to maintain legal guarding position without reaching or bumping."
    },
    {
        "id": 29,
        "questionText": "If a team has excellent defense but poor shooting, what area should they focus on to win more games?",
        "options": ["Rebounding", "Passing", "Shooting accuracy", "Foul drawing"],
        "correctAnswerIndex": 2, # C
        "explanation": "Improving offensive conversion (shooting accuracy) complements elite defensive performance."
    },
    {
        "id": 30,
        "questionText": "In official FIBA play, the height of the basketball ring from the floor is:",
        "options": ["9 feet", "10 feet", "11 feet", "12 feet"],
        "correctAnswerIndex": 1, # B. 10 feet (3.05m)
        "explanation": "Regulation rim height in FIBA and NBA competition is 10 feet above the floor."
    },
    {
        "id": 31,
        "questionText": "Volleyball was invented by William G. Morgan in what year?",
        "options": ["1875", "1895", "1905", "1910"],
        "correctAnswerIndex": 1, # B. 1895
        "explanation": "William G. Morgan invented volleyball in 1895 at Holyoke, Massachusetts."
    },
    {
        "id": 32,
        "questionText": "Volleyball was originally called:",
        "options": ["Handball", "Netball", "Mintonette", "Spikeball"],
        "correctAnswerIndex": 2, # C. Mintonette
        "explanation": "Volleyball was originally named Mintonette before being renamed due to its volleying nature."
    },
    {
        "id": 33,
        "questionText": "How many players are on each volleyball team during play?",
        "options": ["5", "6", "7", "8"],
        "correctAnswerIndex": 1, # B. 6
        "explanation": "Indoor volleyball is played with 6 active players per team on court."
    },
    {
        "id": 34,
        "questionText": "The maximum number of times a team may hit the ball before sending it over the net is:",
        "options": ["2", "3", "4", "Unlimited"],
        "correctAnswerIndex": 1, # B. 3
        "explanation": "A team is allowed a maximum of 3 hits to return the ball across the net."
    },
    {
        "id": 35,
        "questionText": "A player may not hit the ball twice in succession unless:",
        "options": [
            "The ball touches the net",
            "It is during a block",
            "The referee allows it",
            "It is during a spike"
        ],
        "correctAnswerIndex": 1, # B
        "explanation": "A block contact does not count as a hit, allowing the blocker to make the team's first hit."
    },
    {
        "id": 36,
        "questionText": "The first team to reach how many points (with at least 2-point lead) wins a standard set?",
        "options": ["21", "23", "25", "30"],
        "correctAnswerIndex": 2, # C. 25
        "explanation": "Standard non-deciding sets in rally scoring are played to 25 points."
    },
    {
        "id": 37,
        "questionText": "What is the main purpose of the serve in volleyball?",
        "options": [
            "To set the ball for a teammate",
            "To put the ball into play",
            "To defend the court",
            "To confuse the opponents"
        ],
        "correctAnswerIndex": 1, # B
        "explanation": "The serve initiates rally play by driving the ball over the net into the opponent's court."
    },
    {
        "id": 38,
        "questionText": "The skill used to position the ball for a teammate’s attack is:",
        "options": ["Pass", "Serve", "Set", "Block"],
        "correctAnswerIndex": 2, # C. Set
        "explanation": "Setting overhead delivers an accurate high trajectory for an attacker to spike."
    },
    {
        "id": 39,
        "questionText": "The most powerful offensive move, hitting the ball downward into the opponent’s court, is called a:",
        "options": ["Spike", "Dig", "Toss", "Bump"],
        "correctAnswerIndex": 0, # A. Spike
        "explanation": "A spike is a hard-driven forceful downward attack hit."
    },
    {
        "id": 40,
        "questionText": "The rotation system in volleyball moves players:",
        "options": ["Clockwise", "Counterclockwise", "Randomly", "By coach’s decision only"],
        "correctAnswerIndex": 0, # A. Clockwise
        "explanation": "Teams rotate clockwise when winning back service possession from the opponent."
    },
    {
        "id": 41,
        "questionText": "Volleyball became an official Olympic sport in:",
        "options": ["1948", "1956", "1964", "1972"],
        "correctAnswerIndex": 2, # C. 1964
        "explanation": "Volleyball was officially introduced to the Olympic program at the 1964 Tokyo Games."
    },
    {
        "id": 42,
        "questionText": "The serving player hits the ball and it lands directly on the opponent’s court untouched. What is this called?",
        "options": ["Spike", "Ace", "Fault", "Dig"],
        "correctAnswerIndex": 1, # B. Ace
        "explanation": "An ace is a serve that results directly in a point without being touched by the receiver."
    },
    {
        "id": 43,
        "questionText": "The ball touches the net during a serve but still goes over and lands inside the opponent’s court. What happens?",
        "options": [
            "The serve counts and play continues",
            "The serve is repeated",
            "The server loses the point",
            "The referee gives a warning"
        ],
        "correctAnswerIndex": 0, # A
        "explanation": "Under modern let-serve rules, a serve touching the net and landing in-bounds remains live."
    },
    {
        "id": 44,
        "questionText": "A team often loses points because their spiker hits the ball out of bounds. Which skill should the coach prioritize during training?",
        "options": [
            "Serve accuracy",
            "Ball control and timing during the spike",
            "Blocking form",
            "Digging and floor defense"
        ],
        "correctAnswerIndex": 1, # B
        "explanation": "Proper wrist snap, contact angle, and approach timing ensure spikes land inside boundaries."
    },
    {
        "id": 45,
        "questionText": "In a crucial rally, the back-row player jumps and spikes the ball in front of the attack line. What should the referee decide?",
        "options": [
            "Legal play, continue rally",
            "Fault—back-row attack violation",
            "Replay the point",
            "Award a time-out"
        ],
        "correctAnswerIndex": 1, # B
        "explanation": "Back-row players cannot complete an attack hit above net height if taking off on or in front of the 3-meter line."
    },
    {
        "id": 46,
        "questionText": "A pitcher keeps throwing high balls, missing the strike zone. Which adjustment would most likely help him improve accuracy?",
        "options": [
            "Decrease pitching speed and adjust release point",
            "Move closer to the batter",
            "Swing the bat slower",
            "Change gloves"
        ],
        "correctAnswerIndex": 0, # A
        "explanation": "Modulating velocity and correcting the mechanical release point directly fixes height trajectory errors."
    },
    {
        "id": 47,
        "questionText": "During a close game, a batter decides to bunt instead of swing. Why might this be a strategic decision?",
        "options": [
            "To hit a home run",
            "To advance a base runner safely",
            "To waste time",
            "To get a strikeout intentionally"
        ],
        "correctAnswerIndex": 1, # B
        "explanation": "A sacrifice bunt intentionally moves a lead runner to the next base in close game situations."
    },
    {
        "id": 48,
        "questionText": "The team’s outfielders are catching fewer fly balls. What is the most likely reason?",
        "options": [
            "Poor communication and misjudged ball trajectory",
            "Too much focus on batting",
            "Weak throwing arm",
            "Small field dimensions"
        ],
        "correctAnswerIndex": 0, # A
        "explanation": "Miscommunicating priority calls and misreading airborne arc trajectories cause dropped fly balls."
    },
    {
        "id": 49,
        "questionText": "The batter hits the ball and runs to first base before the fielders catch it. What should the batter do?",
        "options": [
            "Stop running",
            "Continue running to second base",
            "Stay safely on first base",
            "Leave the field"
        ],
        "correctAnswerIndex": 2, # C
        "explanation": "Once safely touching first base before defensive control, the runner secures first base."
    },
    {
        "id": 50,
        "questionText": "The pitcher throws a ball and it passes outside the strike zone without the batter swinging. What should the umpire call?",
        "options": ["Strike", "Ball", "Out", "Hit"],
        "correctAnswerIndex": 1, # B. Ball
        "explanation": "A pitch outside the strike zone that is unswung by the batter is called a ball."
    }
]

print(f"Verified Section 1 count: {len(q_list)}")
