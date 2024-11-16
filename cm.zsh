(){
    local TEMP_FILE=$(mktemp)
    \cm --out-cd-path $TEMP_FILE $*
    local CD_PATH=$(cat $TEMP_FILE)
    if [[ -n $CD_PATH ]]; then
        cd $CD_PATH
    fi
} $*
