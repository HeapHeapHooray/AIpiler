if [ -f "1-Documentation/ARCHITECTURE.md" ]; then
    echo "ARCHITECTURE.md exists, not running init.sh"
else
    echo "ARCHITECTURE.md doesn't exists, running init.sh"
    bash 1-Documentation/init.sh
fi

ralph "
Run 1-Documentation/per-function.sh .
If there is any listed function that is not defined in 1-Documentation/ARCHITECTURE.md, then task is not complete." --allow-all
