# function __open_completions
#   set -l completions (open -l)
#   for completion in $completions
#     set -a reply $completion
#   end
# 	return $completion
# end

# complete -c o -f -a "(__open_completions)"
complete -c o -f -a "(o -l)"