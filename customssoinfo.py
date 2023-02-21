import boto3
import csv

# Configure the AWS SSO Admin client
sso_admin = boto3.client('sso-admin')
sso_identity = boto3.client('identitystore')

# Replace <INSTANCE_ARN> with the ARN of your SSO instance
instance_arn = ''
identitystore = ''

# Retrieve all the SSO groups for the instance
groups_response = sso_identity.list_groups(IdentityStoreId=identitystore)
groups = groups_response['Groups']
print(groups_response)

# Retrieve all the SSO users for the instance
users_response = sso_identity.list_users(IdentityStoreId=identitystore)
users = users_response['Users']
print(users_response)

# Retrieve all the SSO account assignments for the instance
account_assignments_response = sso_admin.list_account_assignments(InstanceArn=instance_arn,AccountId='',PermissionSetArn='')
account_assignments = account_assignments_response['AccountAssignments']
print(account_assignments_response)


# Retrieve all the SSO permission sets for the instance
permission_sets_response = sso_admin.list_permission_sets(InstanceArn=instance_arn)
permission_sets = permission_sets_response['PermissionSets']
print(permission_sets_response)
#perm_set_dict = {}

while "NextToken" in permission_sets_response:
        permission_sets_response = sso_admin .list_permission_sets(InstanceArn=instance_arn, NextToken=permission_sets_response["NextToken"])
        permission_sets.extend(permission_sets_response["PermissionSets"])




#print(permission_sets_response)

# Write the SSO data to a single CSV file
with open('sso_dt.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Type', 'Id', 'DisplayName', 'Description','PrincipalId','PrincipalType'])

    # Write the SSO groups to the CSV file
    for group in groups:
        writer.writerow(['Group', group['GroupId'], group['DisplayName'], group['Description']])

    # Write the SSO users to the CSV file
    for user in users:
        writer.writerow(['User', user['UserId'], user['DisplayName'],'',''])

    # Write the SSO account assignments to the CSV file
    for account_assignment in account_assignments:
        writer.writerow(['Account Assignment', account_assignment['PermissionSetArn'], '', '', account_assignment['PrincipalId'], account_assignment['PrincipalType']])

    # Write the SSO permission sets to the CSV file
    for permission_set in permission_sets:
        #print(permission_set)
        # get the name of the permission set from the arn
        perm_description = sso_admin.describe_permission_set(InstanceArn=instance_arn,PermissionSetArn=permission_set)
        # key: permission set name, value: permission set arn
        #perm_set_dict[perm_description["PermissionSet"]["Name"]] = permission_set

    print(perm_description)
    
   

    writer.writerow(['Permission Set', permission_set['PermissionSetArn'], permission_set['DisplayName'],permission_sets['Description']])

# Print a message indicating that the export is complete
print("SSO data has been exported to a single CSV file.")


