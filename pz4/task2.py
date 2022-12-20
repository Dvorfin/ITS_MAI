import os
import git

path_to_read = '/home/toor/ITS_MAI/pz4/git.txt'     # path to read gits
path_to_clone = '/home/toor/ITS_MAI/pz4/git_repos'  # path to clone read gits
path_to_write = '/home/toor/ITS_MAI/pz4/result.txt'     # path to repo


def read_git_repos_from_file(path_to_read):
    #print(os.getcwd())
    data = []
    if not os.path.exists(path_to_read):    # check if path exist
        print('File not found')
    else:                                   # if exist -> reading it
        with open (path_to_read, 'r') as f:
            data = f.readlines()
            data = [val.strip() for val in data]  #  delets '\n', ' '
            return data



def clone_git_repos(lst_of_repos, path_to_clone_repo, status):
    for git_url in lst_of_repos:    
        try:
            git.Repo.clone_from(git_url, path_to_clone_repo)    # trying to clone

        except Exception as error:              
            status.setdefault(git_url, 'Fail')      # adding status

        else:
            status.setdefault(git_url, 'OK')

        finally:
            print('work done')


def make_report(path, dict):    #   making report
    with open (path, 'w') as f:
        f.write("Result of copying git repos:\n")
        for key, val in dict.items():
            f.write(f'Repo: {key}   | status: {val}\n')     # writing status for each git Ok/Fail


def main():
    res_status = {}    # dictionary for status

    repos = read_git_repos_from_file(path_to_read)  # list of git repos
   # print(repos)

    clone_git_repos(repos, path_to_clone, res_status)   # cloning repos

    #print(*res_status.keys(), sep='\n')

    make_report(path_to_write, res_status)      # making report

if __name__ == '__main__':
    main()
    