for dir in $(ls -d */)
do
    cd $dir;
    git rm -r __pycache__;
    cp ../remove_cache.sh .;
    bash remove_cache.sh;
    rm remove_cache.sh;
    cd ..;
done
