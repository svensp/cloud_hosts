PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

*/1 * * * * root touch {{ path }} && curl -s https://heartbeat.uptimerobot.com/m784348505-55a0af482c08e873ea565440df512d75511c135c > /dev/null 2>&1
