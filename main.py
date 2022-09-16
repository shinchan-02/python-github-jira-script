from jira import JIRA
from github import Github 


def add_user_to_organization(member, error_count, comment):
    try:
        comment1 = []
        user_to_org = git_hub.get_organization(org_name)
        user_to_org.invite_user(member)
        comment1.append("Invitation has been sent to the user --> {}".format(mail))
        comment.append("{}".format(comment1))
    
    except Exception as error:
        comment1 = []
        comment1.append("Exception --> {}".format(error))
        comment.append("{}".format(comment1))
        #jira.add_comment(issueKey, body="Exception --> {}".format(error))
        error_count += 1
        
    return error_count, comment

        
def add_user_to_team(members, teams_dic, error_count, comment):
    try:
        for team in teams_dic:
            if team:
                for member in members:
                    if member:
                        comment1 = []
                        total_Count = 0
                        try:
                            
                            org_team_ = git_hub.get_organization(org_name).get_team_by_slug(team)
                            total_count = org_team_.invitations().totalCount
                            print(type(total_count))
                            print("total_count = ", total_count)
                            user = git_hub.get_user(member)
                            print("adding user in a team ......", member)
                            user_to_team = org_team_.add_membership(user)
                            
                            if user_to_team is None:
                                print("user_to_team = ", user_to_team)
                                print("org_team_.invitations().totalCount = ", org_team_.invitations().totalCount)
                                print(org_team_.invitations().totalCount == total_Count)
                                print(type(org_team_.invitations().totalCount))
                                var1 = total_count
                                var2 = org_team_.invitations().totalCount
                                if var1 == var2:
                                    comment1.append("User {} has been Added to the team --> {}".format(user, team))
                                    comment.append("{}".format(comment1))
                                    print("org_team_.invitations().totalCount = ", org_team_.invitations().totalCount)
                                    # jira.add_comment(issueKey, body="User {} has been Added to the team --> {}".format(user, team))
                                    print("User Has Been Added")
                                else:
                                    for i in org_team_.invitations():
                                        if i.login == member:
                                            comment1.append("Invitation has been sent to the user --> {}".format(member))
                                            comment.append("{}".format(comment1))
                                            # jira.add_comment(issueKey, body="Invitation has been sent to the user --> {}".format(member))
                                            print("User Has Been Invited")
                            else:
                                comment1.append("Some error Occured --> {}, {}, {}".format(user_to_org, team, member))
                                comment.append("{}".format(comment1))
                                # jira.add_comment(issueKey, body="Some error Occured --> {}, {}, {}".format(user_to_org, team, member))
                                error_count += 1
                                print(user_to_team)
                        except Exception as error:
                            comment1.append("Exception --> {}, {}, {}".format(error, team, member))
                            comment.append("{}".format(comment1))
                            # jira.add_comment(issueKey, body="Exception --> {}, {}, {}".format(error, team, member))
                            error_count += 1
                            print(error)
        return error_count, comment  
    except Exception as error:
        comment1 = []
        comment1.append("Exception --> {}".format(error))
        comment.append("{}".format(comment1))
        #jira.add_comment(issueKey, body="Exception --> {}".format(error))
        error_count += 1
        print(error)
        return error_count, comment
        

        
def add_user_to_organization_with_repo(member, permission, error_count, comment):
    comment1 = []                                      
    try:
        user_to_org = git_hub.get_organization(org_name)
        user = git_hub.get_user(member)
        # print(user_to_org.add_to_members(user, role=permission))
        print(user_to_org.add_to_members(user))
        if user_to_org is not None:
            comment1.append("Invitation has been sent to the user --> {}".format(member))
            comment.append("{}".format(comment1))
        else:
            comment1.append("Some error Occured --> {},{}".format(user_to_org, member))
            comment.append("{}".format(comment1))
            error_count += 1
            print(user_to_org)
            
        return error_count, comment
    except Exception as error:
        comment1.append("Exception --> {}".format(error))
        comment.append("{}".format(comment1))
        #jira.add_comment(issueKey, body="Exception --> {}".format(error))
        error_count += 1
        print(error)
        return error_count, comment

        
        
def add_user_to_repo(members, repos, permission, error_count, comment):                                     
    try:
        for member in members:
            if member:
                user_to_org = git_hub.get_organization(org_name)
                user = git_hub.get_user(member)
                mem_exist = user_to_org.has_in_members(user)

                if mem_exist:
                    print(mem_exist)
                else:
                    error_count, comment = add_user_to_organization_with_repo(member, permission, error_count, comment)

                for repo in repos:
                    if repo:
                        comment1 = []
                        try:
                            org = git_hub.get_organization(org_name).get_repo(repo)
                            user_to_repo = org.add_to_collaborators(member, permission=permission)
                            if user_to_repo is None:
                                print(member, " Has Been Added In ", repo)
                                comment1.append("{0} Has Been Added In {1}".format(member, repo))
                                comment.append("{}".format(comment1))
                                # jira.add_comment(issueKey, body="{0} Has Been Added In {1}".format(member, repo))
                            elif user_to_repo.id:
                                comment1.append("{0} Invited {1}".format(member, repo))
                                comment.append("{}".format(comment1))
                                # jira.add_comment(issueKey, body="{0} Invited {1}".format(member, repo))
                                print(member, " Has Been Invited In ", repo, " With Invite ID : ", user_to_repo.id)
                            else:
                                comment1.append("Some error Occured --> {}, {}, {} ".format(user_to_repo, member, repo))
                                comment.append("{}".format(comment1))
                                # jira.add_comment(issueKey, body="Some error Occured --> {}, {}, {} ".format(user_to_repo, member, repo))
                                error_count += 1
                                print(user_to_repo)
                        except Exception as error:
                            if "https://docs.github.com/rest/reference/repos#get-a-repository" in str(error):
                                comment1.append("Exception --> Repository,[{}], Not Found Please check Repository Name or Github Environment".format(repo))
                                #comment1.append("Exception --> {}, {}, {}".format(error, member, repo))
                                comment.append("{}".format(comment1))
                                # jira.add_comment(issueKey, body="Exception --> {}, {}, {}".format(error, member, repo))
                                error_count += 1
                                print(error)
                            elif "https://docs.github.com/rest" in str(error):
                                comment1.append("Exception --> Repository,[{}], Not Found Please check Repository Name or Github Environment".format(repo))
                                #comment1.append("Exception --> {}, {}, {}".format(error, member, repo))
                                comment.append("{}".format(comment1))
                                # jira.add_comment(issueKey, body="Exception --> {}, {}, {}".format(error, member, repo))
                                error_count += 1
                                print(error)          
                            else:
                                comment1.append("Exception --> {}, {}, {}".format(error, member, repo))
                                comment.append("{}".format(comment1))
                                error_count += 1
                                print(error)
        return error_count, comment
    except Exception as error:
        comment1 = []
        comment1.append("Exception --> {}".format(error))
        comment.append("{}".format(comment1))
        #jira.add_comment(issueKey, body="Exception --> {}".format(error))
        error_count += 1
        print(error)
        return error_count, comment


def add_team_to_repo(teams_dic, repos, permission, error_count, comment):
    try:
        for team in teams_dic:
            print("Team = ", team)
            if team:
                try:
                    org_team = git_hub.get_organization(org_name).get_team_by_slug(team)
                    if org_team.name:
                        for repo in repos:
                            comment1 = []
                            if repo:
                                print("RepoName=", repo)
                                try:
                                    repo_ = git_hub.get_organization(org_name).get_repo(repo)
                                    repo_count = org_team.repos_count
                                    if org_team.update_team_repository(repo_, permission) == True:
                                        comment1.append("Repository --> {0}  Has Been Added into Team --> {1}!!".format(repo, team))
                                        comment.append("{}".format(comment1))
                                        print("Repository --> {0}  Has Been Added into Team --> {1}!!".format(repo, team))

                                except Exception as error:
                                    comment1.append("Github Repository  {} Not found.".format(repo))
                                    comment.append("{}".format(comment1))
                                    # jira.add_comment(issueKey, body="Exception --> {}, {}, {}".format(error, team, repo))
                                    error_count += 1
                                    print(error)
                except Exception as error:
                    comment1 = []
                    #if org_team.name != team:
                    comment1.append("Github Team {} Not found. ".format(team))
                    comment.append("{}".format(comment1))
                    # jira.add_comment(issueKey, body="Exception --> {}".format(error))
                    error_count += 1
                    print(error)
                
        return error_count, comment
    except Exception as error:
        comment1 = []
        comment1.append("Exception --> {}".format(error))
        comment.append("{}".format(comment1))
        # jira.add_comment(issueKey, body="Exception --> {}".format(error))
        error_count += 1
        print(error)
        return error_count, comment
            


def user_to_branch_protection_rule(members, repos, branches, error_count, comment):
    try:
        for member in members:
            if member:
                for repo in repos:
                    if repo:
                        for branch in branches:
                            if branch:
                                comment1 = []
                                try:
                                    org = git_hub.get_organization(org_name).get_repo(repo)
                                    branch_protection = org.get_branch(branch)
                                    response = branch_protection.add_user_push_restrictions(member)
                                    if response == None:
                                        comment1.append("Merge Access Provided for {} Branch to User {}".format(branch,member))
                                        comment.append("{}".format(comment1))
                                        print(response)
                                except Exception as error:
                                    comment1.append("Exception --> {}, {}, {}, {}".format(error, member, repo, branch))
                                    comment.append("{}".format(comment1))
                                    # jira.add_comment(issueKey, body="Exception --> {}, {}, {}, {}".format(error, member, repo, branch))
                                    error_count += 1
                                    print(error)
        return error_count, comment
    except Exception as error:
        comment1 = []
        comment1.append("Exception --> {}".format(error))
        comment.append("{}".format(comment1))
        #jira.add_comment(issueKey, body="Exception --> {}".format(error))
        error_count += 1
        print(error)
        return error_count, comment


def create_repo(github_members, git_permission, repository, description, error_count, comment):
    comment1 =[]
    try:
        organization = git_hub.get_organization(org_name)
        for name in repository:
            print(name)
            organization.create_repo(name, description=description, private=True)
            print(organization)
            if organization:
                comment1.append("Response -->  Repository Has Been Created !! {}".format(organization))
                comment.append("{}".format(comment1))
                if github_members is not None:
                    error_count, comment = add_user_to_repo(github_members, repository, git_permission, error_count, comment)
                # jira.add_comment(issueKey, body="Repository --> {} Has Been Created !! {}".format(name, organization))
        return error_count, comment

    except Exception as error:
        comment1.append("Exception --> {}".format(error))
        comment.append("{}".format(comment1))
        # jira.add_comment(issueKey, body="Exception --> {}".format(error))
        error_count += 1
        print(error)
        return error_count, comment
   

def create_team(github_team, github_members, git_permission, repository, error_count, comment):
    comment1 = []
    for team in github_team:
        try:
            org = git_hub.get_organization(org_name).create_team(name=team, privacy='closed')
            print(org)
            
            comment1.append("Response -->  Team Has Been Created !! {}".format(team))
            comment.append("{}".format(comment1))
            
        except Exception as error:
            comment1.append("Exception --> {}".format(error))
            comment.append("{}".format(comment1))
            # jira.add_comment(issueKey, body="Exception --> {}".format(error))
            error_count += 1
            print(error)
    
    return error_count, comment
            
            
    if error_count == 0 and github_members is not None :
        print("members = ", github_members)
        print("teams_dic = ", github_team)
        print('Add_user_to_team')
        
        error_count, comment = add_user_to_team(github_members, github_team, error_count, comment)
            
    if error_count == 0 and repository is not None :
        print("teams_dic = ", github_team)
        print("repos = ", repository)
        print('Add_team_to_repo')

        error_count, comment = add_team_to_repo(github_team, repository, git_permission, error_count, comment)
            
            
        
def create_branch_protection_rule(repos,branches, error_count, comment):
    for repo in repos:
        for branch in branches:
            comment1 = []
            try:
                org = git_hub.get_organization(org_name).get_repo(repo).get_branch(branch)
                print(org)
                org.edit_protection(required_approving_review_count=2)
                print(org.get_protection())
                comment1.append("Branch Protection Rule Created for Branch {}  in Repository {} \n {}".format(branch, repo, org.get_protection())) 
                comment.append(comment1)
            except Exception as e:
                error_count += 1
                print("Error = ", e)
                comment1.append("Branch Protection Rule can not be Created for Branch {}  in Repository {} \n {}".format(branch, repo, e())) 
                comment.append(comment1)
               
    return error_count, comment


if __name__ == "__main__":

    USERNAME = #github_username
    access_token = #github_token
    git_hub = Github(USERNAME, access_token)
    org_name = #github_organisation_name

    jiraOptions = {'server': #jira_url}
    jira = JIRA(options=jiraOptions, basic_auth=(#jira_sername, #jira_token))

    count = 0
    exit_count = 0
    issue_ = []

    for singleIssue in jira.search_issues(jql_str='project = #ProjectName and labels = github '):
        count += 1
        
        issueKey = singleIssue.key
        error_count = 0
        comment = []
        member_not_exist = 0
        invalid_email = 0

        f = jira.fields()
        issue = jira.issue(issueKey)
        idnameMap = {jira.field['name']: jira.field['id'] for jira.field in f}
        
        try:

            Github_Action = getattr(issue.fields, idnameMap["Action"])  #getting Action from jira dropdown 
            Github_Action = str(Github_Action)

            Github_User = getattr(issue.fields, idnameMap["UserName"])  #getting usernmae from jira field
            if Github_User is not None:
                github_members = [str(i.replace(' ', '')) for i in Github_User.strip().split(",")] 
                #making it list to get multipple user at a time
                else:
                    github_members = None

           Github_Repo = getattr(issue.fields, idnameMap["Repo Name"])
           if Github_Repo is not None:
               repository = [str(i.replace(' ', '')) for i in Github_Repo.strip().split(",")]
           else:
               repository = None
               
               
           Github_Team = getattr(issue.fields, idnameMap["Team Name"])
           if Github_Team is not None:
               github_team = [str(i.replace(' ', '')) for i in Github_Team.strip().split(",")]
           else:
               github_team = None
               
           Github_Branch = getattr(issue.fields, idnameMap["Branch Name"])
           if Github_Branch is not None:
               github_branch = [str(i.replace(' ', '')) for i in Github_Branch.strip().split(",")]
           else:
               github_branch = None
           
           Github_Permission = getattr(issue.fields, idnameMap["permission"])
           git_permission = str(Github_Permission).lower()
           
           if Github_Action is None :
               comment.append("Required fields Action is missing. Please Fill all the required Fields.")
               error_count += 1
           else:
               if github_members is not None and Github_Action != 'Add_user_to_org':
                   comment1 = []
                   
                   for member, mail in github_members:
                       #check if member already exist
                       org = git_hub.get_organization(org_name)
                       user = git_hub.get_user(member)
                       mem_exist = org.has_in_members(user)
                       if not mem_exist :
                           comment1.append("Memebr doesn't exist --> {}".format(member))
                           
               if Github_Action == 'Add_user_to_org':
                   print('Add_user_to_org')
                   if github_members is not None:
                       for member in github_members:
                           error_count, comment = add_user_to_organization(member, error_count, comment)
                   else:
                       error_count += 1
               
               if Github_Action == 'Add_user_to_team':
                   print('Add_user_to_team')
                   if github_members is not None and github_team is not None:
                       error_count, comment = add_user_to_team(github_members, github_team, error_count, comment)
                   else:
                       error_count += 1
                       
               if Github_Action == 'Add_team_to_repo':
                   print('Add_team_to_repo')
                   if repository is not None and github_team is not None and git_permission is not None:
                        error_count, comment = add_team_to_repo(github_team, repository, git_permission, error_count, comment)
                   else:
                       error_count += 1
                                
               if Github_Action == 'Add_user_to_repo':
                   print('Add_user_to_repo')
                   if repository is not None and github_members is not None and git_permission is not None :
                       error_count, comment = add_user_to_repo(github_members, repository, git_permission, error_count, comment)
                   else:
                       error_count += 1
                                
               if Github_Action == 'Add_User_to_Branch_Protection_Rule':
                   print('Add_User_to_Branch_Protection_Rule')
                   if repository is not None and github_members is not None and github_branch is not None:
                       error_count, comment = user_to_branch_protection_rule(github_members, repository, github_branch, error_count, comment)
                   else:
                       error_count += 1
                            
               if Github_Action == 'Create_repo':
                   desc = "Created by JIRA  {}".format(issueKey)
                   print('Create_repo')
                   if repository is not None:
                       error_count, comment = create_repo(github_members, git_permission, repository, desc, error_count, comment)
                   else:
                       error_count += 1

               if Github_Action == 'Create_team':
                   print("Create_team")
                   if github_team is not None:
                       error_count, comment = create_team(github_team, github_members, git_permission, repository, error_count, comment)
                   else:
                       error_count += 1
                                
               if Github_Action == 'Create_Branch_Protection_Rule':
                   print('create_branch_protection_rule')                            
                   if repository is not None and  github_branch is not None:
                       error_count, comment = create_branch_protection_rule(repository, github_branch, error_count, comment)
                   else:
                       error_count += 1
                                
        except Exception as e:
            print("Main Exception")
            comment.append("|| Automation ||\n|{}|".format(e))
            error_count += 1
            print(e)
        
        
        if error_count == 0 :
           #comment & closing the jira
        
            print("Success : {}".format(issueKey))
            
            var = ''
            for c in comment:
                var = var + '\n |{}|'.format(c)
            print(var)
            
            #comment in jira
            jira.add_comment(issueKey, body="|| Automation [Successful] ||\n|{}|".format(var))
            #transition in jira
            jira.transition_issue(issueKey, #transtion_state_according_to_your_jira_project_in {nmbers})
           
        else:
            # only comment in jira 
            var_count = 0
            print("ERROR COUNT : ", error_count)
            print("Failed : {}".format(issueKey))
            exit_count += 1
            
            var = ''
            for c in comment:
                var_count += 1
                    var = var + '\n |{}|{}|'.format(var_count, c)
                    #add_comment_var = "|| Automation || \n |{}|".format(c) 
                print(var)
                
                jira.add_comment(issueKey, body="|| Automation [Failed] ||\n|{}|".format(var))

             
    if count == 0:
        print("NO Labels found with  github !!!")  
    else:
        if exit_count != 0 :
            print("Exit COUNT : ", exit_count)
            #to failed the job in case of any missing parameter
            sys.exit(exit_count)
