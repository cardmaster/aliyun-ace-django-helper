#!/bin/bash

APP_ROOT=approot
CP_FOLDERS="locale common"
DEPLOY_SPECIALS="app.yaml index.py"


function myreadlink() {
  (
  cd $(dirname $1)         # or  cd ${1%/*}
  echo $PWD/$(basename $1) # or  echo $PWD/${1##*/}
  )
}

SCR_DIR=$(dirname $(myreadlink $0))

target=$1
if [ -z $target ]; then
	echo "NO TARGET"
	exit 1
fi

if [ ! -d ${target} ]; then
	echo "TARGET not a folder"
	exit 1
fi

source=$2
if [ -z $source ]; then
	source=$(myreadlink ${SCR_DIR}/..)
fi

echo Deploy from "${source}" to "${target}"

#work in temporary folder
TEMP_DEPLOY=${SCR_DIR}/.deploytemp
if [ -e ${TEMP_DEPLOY} ]; then
	rm -rf ${TEMP_DEPLOY}
fi
mkdir -p ${TEMP_DEPLOY}

cp -rf ${SCR_DIR}/static ${TEMP_DEPLOY}/

for folder in ${CP_FOLDERS} ${APP_ROOT}; do
	cp -r ${source}/${folder} ${TEMP_DEPLOY}/
	if [ -d ${TEMP_DEPLOY}/${folder}/static ]; then
		echo "collecting static files from "${folder}
		mv ${TEMP_DEPLOY}/${folder}/static/* ${TEMP_DEPLOY}/static/
		rm -rf ${TEMP_DEPLOY}/${folder}/static
	fi
done

cp ${SCR_DIR}/settings.py ${TEMP_DEPLOY}/${APP_ROOT}
for specf in ${DEPLOY_SPECIALS}; do	
	cp ${SCR_DIR}/${specf} ${TEMP_DEPLOY}/
done

find ${TEMP_DEPLOY} -name "*.pyc" -delete
find ${TEMP_DEPLOY} -name "migrations" -delete

function minify() {
JS_WARN=./jswarn.log

for f in $(find ${TEMP_DEPLOY}/static -name "*.js"); do 
	echo -n "COMRESSING " $(basename ${f}) " ... "
	if [ $(echo $f | grep -e '\.min\.js$') ]; then
		echo "   ALREADY COMPRESSED"
	else
		echo FILE $f >> ${JS_WARN}
		uglifyjs -c -m -o ${f}.min ${f} >>${JS_WARN} 2>&1
		mv -f ${f}.min ${f}
		echo "   DONE"
	fi
done
echo js minify logs here: ${JS_WARN}
for f in $(find ${TEMP_DEPLOY}/static -name "*.css"); do 
	echo "COMRESSING" $(basename ${f})
	cssmin ${f} > ${f}.min
	mv -f ${f}.min ${f}
done
}

function stripstatic() {
USE_STATIC_LIST=$(grep -e '{%\s*load\s\+staticfiles\s*%}' -lr ${TEMP_DEPLOY})
sq="'"
for f in ${USE_STATIC_LIST}; do
	echo 'handle static' $(basename $(dirname $f))/$(basename $f)
	sed -i .tmp -e 's,{%[[:space:]]*load[[:space:]]*staticfiles[[:space:]]*%},,' $f 
	grep -e '{%\s*load\s\+staticfiles\s*%}' $f 

	sed -i .tmp -e 's,{%[[:space:]]*static[[:space:]]*['$sq'"]\([[:alnum:]/_]*\.[[:alnum:]]*\)["'$sq'"][[:space:]]*%},/static/\1,g' $f
	grep -e '{%\s*static\s\+['$sq'"].\+['$sq'"]\s*%}' $f 
	
	rm -f $f.tmp
done

}

minify
stripstatic

cp -rf ${TEMP_DEPLOY}/* ${target}/
rm -rf ${TEMP_DEPLOY}

echo "DONE"
echo ${target} is ready for svn operation

