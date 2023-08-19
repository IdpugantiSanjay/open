#!/usr/bin/env bash


# Reference: https://iridakos.com/programming/2018/03/01/bash-programmable-completion-tutorial

#_open_completions() {
#  if [ "${#COMP_WORDS[@]}" != "2" ]; then
#    return
#  fi
#  COMPREPLY=($(compgen -W "$(open -l)" -- "${COMP_WORDS[1]}"))
#}


_open_completions() {
  COMPREPLY=()
  word_count=${#COMP_WORDS[@]}
  options="$(open -l -p "${COMP_WORDS[-1]}")"
  if [ "$word_count" -le 2 ]; then
    while IFS= read -r option; do
      COMPREPLY+=("$option")
    done <<< "$options"
  fi
}

