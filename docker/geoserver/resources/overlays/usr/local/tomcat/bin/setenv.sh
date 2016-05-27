# export CATALINA_OPTS="$CATALINA_OPTS -Xms64m"
# export CATALINA_OPTS="$CATALINA_OPTS -Xmx256m"
# export CATALINA_OPTS="$CATALINA_OPTS -XX:MaxPermSize=128m"

export JAVA_OPTS="$JAVA_OPTS -Xms64m -Xmx512M -XX:MaxPermSize=128M"
export JAVA_OPTS="$JAVA_OPTS -Djava.awt.headless=true -XX:+UseConcMarkSweepGC -XX:+CMSClassUnloadingEnabled"
