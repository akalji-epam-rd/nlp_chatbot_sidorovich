## greet
* greet
  - utter_greet

## describe
* describe
  - utter_describe

## ask_question
* info_question{"info":"Otter"}
  - answer_question
  - slot{"info": null}

## anec_
* anecdote{"anecdote_theme":"mutant"}
  - tell_an_anecdote
  - slot{"anecdote_theme": null}
* laugh
  - utter_not_fun

## not fun
* laugh
  - utter_not_fun

## story_sell
* sell
 - utter_sell

## say goodbye
* goodbye
  - action_goodbye

## story offer
* offer
  - utter_offer
 
## story buy_cost
* buy{"money": null}
  - action_sleep
* buy_cost
  - action_buy_cost
  - slot{"money" : null}

## story buy_cost2
* buy_cost
  - action_check
  
## story sleep
* sleep
  - action_sleep
  - slot{"money" : null}
* buy_cost
  - action_buy_cost
  - slot{"money" : null}
 
## can_hide story
* can_hide
  - action_check_hideaway

## where_hide story
* where_hide
  - action_find_hideaway

## last emission story
* when_was
  - action_last_emission

## future emission story
* when_will
  - action_future_emission