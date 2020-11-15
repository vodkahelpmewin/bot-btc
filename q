#!/bin/bash
  
export TOKEN=614428243:AAHJ1bdBnhlO5q_w0BNOB10BoALCcXpFSlA
export CHAT_ID=291140894
export URL="https://api.telegram.org/bot614428243:AAHJ1bdBnhlO5q_w0BNOB10BoALCcXpFSlA/sendMessage"
export MESSAGES=$1
curl -s -X POST $URL -d chat_id=$CHAT_ID -d text="$1"
