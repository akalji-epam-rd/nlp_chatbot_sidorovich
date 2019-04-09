
## story 1
* greet
  - memory_visit
  - slot{"id" : "1"}
  
## story 2
* greet
  - memory_visit
  - slot{"id" : "5"}
  
## story 3
* greet
  - memory_visit
  - slot{"id" : "19"}
  
## story 4
* sell{"info":"Otter"}
 - sell_request

## story 4
* greet
  - memory_visit
  - slot{"id" : "56"}

## story 5
* greet
  - memory_visit
  - slot{"id" : "2"}

## story 6
* greet
  - memory_visit
  - slot{"id" : "100"}

## story 7
* greet
  - memory_visit
  - slot{"id" : "74"}

## story 8
* info_question{"info":"Otter"}
  - answer_question

## story 9
* info_question{"info":"Generators"}
  - answer_question

## story 10
* info_question{"info":"Darkscape"}
  - answer_question

## story 11
* info_question{"info":"Vortex"}
  - answer_question

## story 12
* info_question{"info":"Kazakov"}
  - answer_question


## say goodbye
* goodbye
  - utter_goodbye
  
## dialogue 1
* greet
  - memory_visit
* goodbye
  - utter_goodbye

## dialogue 2
* greet
  - memory_visit
* info_question{"info":"Strelok"}
  - answer_question
* goodbye
  - utter_goodbye
