rm -rf __pycache__;
for dir in $(ls -d */)
do
    cd $dir;
    cp ../remove_cache.sh .;
    bash remove_cache.sh;
    rm remove_cache.sh;
    cd ..;
done
