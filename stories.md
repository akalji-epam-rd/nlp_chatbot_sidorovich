## greet
* greet
  - utter_greet

## describe
* describe
  - utter_describe

## ask_question
* info_question{"info":"Otter"}
  - answer_question

## anec_
* anecdote{"anecdote_theme":"bloodsucker"}
  - tell_an_anecdote
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
  - utter_goodbye

## story offer
* offer
  - utter_offer
 
## story buy
* buy
  - action_buy

## story buy_cost
* buy
  - action_buy
* buy_cost
  - action_buy_cost
  
## story sleep
* sleep
  - action_sleep
 
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