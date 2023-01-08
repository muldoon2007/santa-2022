import sys
from colored import fg, bg, attr
import getpass

s="🎅"
t="👹"

prompts={
    'welcome':
    'Hi, kids! I have prepared a friendly challenge for you this year to put your growing brains to the ultimate test. If you pass, you will prove your worthiness for the bounty of gifts I found by your tree last night. If not, well, there\'s always next year!\n\n    Your first quest is this. Find the circuit in the office, and tell me which position dropped the bomb.\n\n',
    'bomb': 'Which position dropped the bomb?',
    'map_clue' : 'QUITE CORRECT! I see you have snapped the circuits. Bravo. Now, for your next challenge:\n\n     Find a place where the waves are small\n     And that\'s why they are equipped to give energy to all.\n     When you\'re there, you will find images and so\n     It will show you the THREE PLACES you can go\n',
    'map' : 'Where would you like to go?',
    'attempt-stadium' : 'You attempt to cross the bridge to enter the stadium, but you are blocked by a hideous troll.',
    'troll-riddle-1' : 'Hello, you puny children!\n\n    I have a nasty riddle for you!\n\n    What was Uncle Phil\'s final message? If this is too hard for you, you can run!',
    'troll-riddle-2' : 'You solved it! Now a truly impossible one for you!\n\n    I lost a secret encoded message. If you find the paper and the hidden message, tell it to me now and I will let you pass!\n\n    I know it was something that represented a person and a place.\n\n    If this is too hard for you, you can run!\n\n    What was the hidden message?',
    'troll-solved' : 'You have cracked my most terrifying riddles! You may now pass to the stadium.'
}

def troll_text(prompt):
    print(f"{fg('yellow')} {t} {prompt}")

def text(prompt, character=s):
    print(f"{fg('green')} {character} {prompt}")

def get_input(prompt, person=s, specified_value=None, expected_answers=None, expected_type=int, hide=False, color='misty_rose_3', hint_expected=True):
    if expected_answers is None:
        expected_answers = []
    response = None
    if specified_value:
        # Value specified, validating user provided input
        if expected_answers:
            if specified_value not in expected_answers:
                print(f"{fg('red')}{specified_value} is an invalid choice. Choose something from {expected_answers}{attr('reset')}")
                end()
        return specified_value

    else:
        # Value not specified, prompt user
        while isinstance(response, expected_type) is False:
            if expected_answers and hint_expected:
                question = input(f"{fg(color)} {person} {prompt} {expected_answers}{attr('reset')}: ")
            else:
                if hide is True:
                    question = getpass.getpass(prompt=f"{fg(color)} {person} {prompt} {expected_answers}{attr('reset')}: ")
                else:
                    question = input(f"{fg(color)} {person} {prompt}{attr('reset')}: ")

            try:
                response = expected_type(question.rstrip().lstrip().lower())
            except ValueError:
                print(f"Sorry, expected answer is something from {expected_answers}")


            if expected_answers:
                if response not in expected_answers:
                    if hide is False:
                        print(f"{fg('red')}\n     You can\'t do that! Try again!\n")
                    if hint_expected:
                        print(f"Choose something from {expected_answers}{attr('reset')}")
                    response = None

    return response

def end():
    text("Merry Christmas! You've gotten all my digital clues. Now go get those goodies! Goodbye.")

def get_next_place(current_place):
    return get_input(prompt=prompts['map'], expected_answers=['farm', 'school', 'stadium'], hint_expected=False, expected_type=str)
    # if result == 'stadium':
    #     if current_place == 'farm':
    #         text('You may not reach the stadium from the farm!')

if __name__ == "__main__":
    state = {'location':'start', 'troll': 'unsolved'}
    text(prompts['welcome'])
    get_input(prompt=prompts['bomb'],expected_answers=["x"], hint_expected=False, expected_type=str)
    text(prompts['map_clue'])
    while state['troll'] != 'solved':
        text(f'You are currently at location: {state["location"]}')
        if state['location'] == 'stadium':
            text(prompts['attempt-stadium'])
            answer1=get_input(prompt=prompts['troll-riddle-1'], person='👹', expected_answers=['run', 'create'], hint_expected=False, expected_type=str)
            if answer1 == 'run':
                state['location']='school'
            elif answer1 == 'create':
                # text(prompts['troll-2'])
                answer2=get_input(prompt=prompts['troll-riddle-2'], person='👹', expected_answers= ['run', 'washington'], hint_expected=False, expected_type=str)
                if answer2 == 'run':
                    state['location']='school'
                elif answer2 == 'washington':
                    state['troll'] = 'solved'
        elif state['location'] == 'start':
            state['location'] = get_next_place(state['location'])
        elif state['location'] == 'farm':
            text('You gaze across a small, beautiful farm. You decide to feed a goat. The goat groans approvingly and begins to talk.')
            text('I am a happy goat today. I would like to help you on your journey to recover these lost gifts.\n\n    Go to a place that is a home of markers\n    Some colors are light, and others are darker\n    You can use them to draw or write or trace\n    But though they all have ink, they can all be erased.\n', '🐐')
            text('The goat leaps away to go hunting for squirrels and food scraps.')
            state['location'] = get_next_place(state['location'])
        elif state['location'] == 'school':
            text('You enter a beatiful, brick school building. You walk around and notice a piece of paper on the floor')
            answer=get_input(prompt='Do you want to read the paper?', expected_answers=['y','n'], expected_type=str)
            if answer=='y':
                text('The paper says:\n\n     In a closet far up high\n     Is a place that is secure\n     If you go and crack it open\n     You will find another clue for sure\n', '📜')
            state['location']= get_next_place(state['location'])
        else:
            get_next_place(state['location'])

    text('I am ashamed. You have defeated me. Please allow me to run away in disgrace. And I will give you a tip that may help you in your journey.\n\n     Go to the place where presents were found last year\n     And you will find a clue appear.\n\n    Come back when you have found it.',t)
    get_input('What was the name of the place that made the Great Shields connect?', person=t, expected_answers=['zanzibar'], hint_expected=False, expected_type=str)
    text('Your intelligence is too great! Please pass now to the stadium\n',t)
    text('You enter the stadium. It is empty. There is a podium in front with a piece of paper and a mysterious note written.\n')
    text('  Go to the place where Layla lies\n      And you will find one last surprise\n','📜')
    circuit_answer=None
    while circuit_answer != 'switch':
        circuit_answer=get_input('What component must go in position C?', expected_answers=['switch','battery','resistor'], hint_expected=False, expected_type=str)
        if circuit_answer == 'battery':
            text('No, but you are getting the right idea!')
        elif circuit_answer == 'resistor':
            text('No cigar, but I like your thinking!')
    text('BRAVO! You have solved almost the whole darn puzzle. Now, how about this one:\n\n      Your male parent has a new tiny drawer\n      I\'ll give you a hint that it\'s not on the first floor.\n')

    end()
