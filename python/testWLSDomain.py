#=======================================================================================
#
#
# Usage:
#      java weblogic.WLST <WLST_script>
#
# Where:
#      <WLST_script> specifies the full path to the WLST script.
#=======================================================================================

adminSvrURL   = 't3://localhost:7007'
adminUsername = 'weblogic'
adminPassword = 'password1234!'
domainDir     = '/Users/tduong/oracle/wls12214/user_projects/domains/basicWLSDomain'

print 'Starting the Admin Server to test...';
try:

    try:
        connect(adminUsername, adminPassword, adminSvrURL)
        print 'Connected to AdminServer'
    except WLSTException:
        startServer(url=adminSvrURL, username=adminUsername, password=adminPassword, domainDir=domainDir)
        print 'Started the Admin Server'

    servers = domainRuntimeService.getServerRuntimes();

    if (len(servers) > 0):
        for server in servers:
            jmsRuntime = server.getJMSRuntime();
            jmsServers = jmsRuntime.getJMSServers();
            jmsServer = jmsServers[0]
            print "Verifying JMSServer..."
            if (jmsServer.getName() != 'myJMSServer'):
                raise WLSTException('Not matched! Expected: myJMSServer, Result: %s' %jmsServer.getName())

    print "Verifying JMSSystemResources..."
    JMSResources = cmo.getJMSSystemResources()
    jmsResource  = JMSResources[0]

    if (jmsResource.getName() != 'myJMSSystemResource'):
        raise WLSTException('Not matched! Expected: myJMSSystemResource, Result: %s' %jmsResource.getName())

    topics = jmsResource.getJMSResource().getTopics()

    print "Verifying Topics..."
    expected_topics = ['jms/myTopic']
    current_topics  = []
    for topic in topics:
        current_topics.append(topic.getJNDIName())
    if len(expected_topics) != len(current_topics):
        raise WLSTException('Not matched! Expected: %s, Result: %s' %(len(expected_topics), len(current_topics)) )

    expected_topics.sort()
    current_topics.sort()

    if expected_topics != current_topics:
        raise WLSTException('Not matched! Expected: %s, Result: %s' %(expected_topics, current_topics) )

    print "SUCCESS"

except WLSTException, e:
    print e
    print "FAILED"

exit()
