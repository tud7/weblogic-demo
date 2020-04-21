#=======================================================================================
# This is an example of a simple WLST offline configuration script. The script creates
# a simple WebLogic domain using the Basic WebLogic Server Domain template. The script
# demonstrates how to open a domain template, create and edit configuration objects,
# and write the domain configuration information to the specified directory.
#
# Usage:
#      java weblogic.WLST <WLST_script>
#
# Where:
#      <WLST_script> specifies the full path to the WLST script.
#=======================================================================================

#=======================================================================================
# Open a domain template.
#=======================================================================================

readTemplate("/Users/tduong/oracle/wls12214/wlserver/common/templates/wls/wls.jar")
#selectTemplate('Base WebLogic Server Domain')
#loadTemplates()

#=======================================================================================
# Configure the Administration Server and SSL port.
#
# To enable access by both local and remote processes, you should not set the
# listen address for the server instance (that is, it should be left blank or not set).
# In this case, the server instance will determine the address of the machine and
# listen on it.
#=======================================================================================

cd('Servers/AdminServer')
set('ListenAddress','')
set('ListenPort', 7007)

#=======================================================================================
# Define the user password for weblogic.
#=======================================================================================

cd('/')
cd('Security/base_domain/User/weblogic')
cmo.setPassword('password1234!')

cd('/Security/base_domain/User')
create('TestUser','User')
cd('/Security/base_domain/User/TestUser')
set('password','password1234!')

#=======================================================================================
# Create a JMS Server.
#=======================================================================================

cd('/')
jmsserver = create('myJMSServer', 'JMSServer')


fstore = create('myFileStore','FileStore')
cd('/FileStore/myFileStore')
set('Directory','/Users/tduong/tmp')

jmsserver.setPersistentStore(fstore)

#=======================================================================================
# Create a JMS System resource.
#=======================================================================================

cd('/')
create('myJMSSystemResource', 'JMSSystemResource')
cd('JMSSystemResource/myJMSSystemResource/JmsResource/NO_NAME_0')

#=======================================================================================
# Create a JMS Topic and its subdeployment.
#=======================================================================================

mytopic = create('myTopic','Topic')
mytopic.setJNDIName('jms/myTopic')
mytopic.setSubDeploymentName('myTopicSubDeployment')

cd('/')
cd('JMSSystemResource/myJMSSystemResource')
create('myTopicSubDeployment', 'SubDeployment')

#=======================================================================================
# Target resources to the servers.
#=======================================================================================

cd('/')
assign('FileStore', 'myFileStore', 'Target', 'AdminServer')
assign('JMSServer', 'myJMSServer', 'Target', 'AdminServer')
assign('JMSSystemResource.SubDeployment', 'myJMSSystemResource.myTopicSubDeployment', 'Target', 'myJMSServer')
#assign('JDBCSystemResource', 'myDataSource', 'Target', 'AdminServer')

#=======================================================================================
# Write the domain and close the domain template.
#=======================================================================================

setOption('OverwriteDomain', 'true')
writeDomain('/Users/tduong/oracle/wls12214/wlserver/../user_projects/domains/basicWLSDomain')
closeTemplate()

#=======================================================================================
# Exit WLST.
#=======================================================================================

exit()
