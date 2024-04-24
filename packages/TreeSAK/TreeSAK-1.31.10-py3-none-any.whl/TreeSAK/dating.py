import os
import argparse
import itertools
from ete3 import Tree
from Bio import AlignIO


dating_usage = '''
======================== Dating example commands ========================

# requireMENT: mcmctree, baseml and codeml (all from PAML)

# example commands
TreeSAK Dating -tree tree.treefile -msa markers.phylip -o dating_wd -f

=========================================================================
'''


def sep_path_basename_ext(file_in):

    f_path, f_name = os.path.split(file_in)
    if f_path == '':
        f_path = '.'
    f_base, f_ext = os.path.splitext(f_name)

    return f_name, f_path, f_base, f_ext[1:]


def root_with_out_group(tree_file, out_group_txt, tree_file_rooted):

    out_group_set = set()
    for each_og in open(out_group_txt):
        out_group_set.add(each_og.strip())

    tre = Tree(tree_file, format=1)
    out_group_lca = tre.get_common_ancestor(out_group_set)
    tre.set_outgroup(out_group_lca)
    tre.write(outfile=tree_file_rooted)


def replace_clades(main_tree, sub_tree, tree_out, quote_node_name):

    tre_sub = Tree(sub_tree, format=1, quoted_node_names=quote_node_name)
    subtree_leaf_name_list = tre_sub.get_leaf_names()
    tre_main = Tree(main_tree)
    lca = tre_main.get_common_ancestor(subtree_leaf_name_list)

    if len(lca.get_leaf_names()) != len(subtree_leaf_name_list):
        print('LCA of subtree leaves in main tree contain extra leaves, program exited!')
        exit()

    lca_p = lca.up
    lca_p.remove_child(lca)
    lca_p.add_child(tre_sub)
    tre_main.write(outfile=tree_out, format=8, quoted_node_names=quote_node_name)


def prep_mcmctree_ctl(ctl_para_dict, mcmctree_ctl_file):

    ctl_file_handle = open(mcmctree_ctl_file, 'w')
    ctl_file_handle.write('          seed = %s\n' % ctl_para_dict.get('seed', '-1'))
    ctl_file_handle.write('       seqfile = %s\n' % ctl_para_dict['seqfile'])
    ctl_file_handle.write('      treefile = %s\n' % ctl_para_dict['treefile'])
    ctl_file_handle.write('      mcmcfile = %s\n' % ctl_para_dict['mcmcfile'])
    ctl_file_handle.write('       outfile = %s\n' % ctl_para_dict['outfile'])
    ctl_file_handle.write('         ndata = %s\n'                                                                           % ctl_para_dict.get('ndata',        1))
    ctl_file_handle.write('       seqtype = %s    	* 0: nucleotides; 1:codons; 2:AAs\n'                                    % ctl_para_dict['seqtype'])
    ctl_file_handle.write('       usedata = %s    	* 0: no data; 1:seq like; 2:normal approximation; 3:out.BV (in.BV)\n'   % ctl_para_dict['usedata'])
    ctl_file_handle.write('         clock = %s    	* 1: global clock; 2: independent rates; 3: correlated rates\n'         % ctl_para_dict.get('clock',        2))
    ctl_file_handle.write('       RootAge = %s      * safe constraint on root age, used if no fossil for root.\n'           % ctl_para_dict.get('RootAge',      '<1.0'))
    ctl_file_handle.write('         model = %s    	* 0:JC69, 1:K80, 2:F81, 3:F84, 4:HKY85\n'                               % ctl_para_dict.get('model',        0))
    ctl_file_handle.write('         alpha = %s  	* alpha for gamma rates at sites\n'                                     % ctl_para_dict.get('alpha',        0.5))
    ctl_file_handle.write('         ncatG = %s    	* No. categories in discrete gamma\n'                                   % ctl_para_dict.get('ncatG',        4))
    ctl_file_handle.write('     cleandata = %s    	* remove sites with ambiguity data (1:yes, 0:no)?\n'                    % ctl_para_dict.get('cleandata',    0))
    ctl_file_handle.write('       BDparas = %s      * birth, death, sampling\n'                                             % ctl_para_dict.get('BDparas',      '1 1 0.1'))
    ctl_file_handle.write('   kappa_gamma = %s      * gamma prior for kappa\n'                                              % ctl_para_dict.get('kappa_gamma',  '6 2'))
    ctl_file_handle.write('   alpha_gamma = %s      * gamma prior for alpha\n'                                              % ctl_para_dict.get('alpha_gamma',  '1 1'))
    ctl_file_handle.write('   rgene_gamma = %s      * gammaDir prior for rate for genes\n'                                  % ctl_para_dict.get('rgene_gamma',  '1 50 1'))
    ctl_file_handle.write('  sigma2_gamma = %s      * gammaDir prior for sigma^2     (for clock=2 or 3)\n'                  % ctl_para_dict.get('sigma2_gamma', '1 10 1'))
    ctl_file_handle.write('      finetune = %s      * auto (0 or 1): times, musigma2, rates, mixing, paras, FossilErr\n'    % ctl_para_dict.get('finetune',     '1: .1 .1 .1 .1 .1 .1'))
    ctl_file_handle.write('         print = %s      * 0: no mcmc sample; 1: everything except branch rates 2: everything\n' % ctl_para_dict.get('print',        1))
    ctl_file_handle.write('        burnin = %s\n'                                                                           % ctl_para_dict.get('burnin',       50000))
    ctl_file_handle.write('      sampfreq = %s\n'                                                                           % ctl_para_dict.get('sampfreq',     50))
    ctl_file_handle.write('       nsample = %s\n'                                                                           % ctl_para_dict.get('nsample',      10000))
    ctl_file_handle.close()


def get_parameter_combinations(para_to_test_dict):

    para_lol_name = []
    para_lol_value = []
    para_lol_name_with_value = []
    for each_para in sorted(list(para_to_test_dict.keys())):
        para_setting_list_name = []
        para_setting_list_value = []
        para_setting_list_name_with_value = []
        for each_setting in sorted(para_to_test_dict[each_para]):
            name_str = ('%s%s' % (each_para, each_setting)).replace(' ', '_')
            para_setting_list_name.append(each_para)
            para_setting_list_value.append(each_setting)
            para_setting_list_name_with_value.append(name_str)
        para_lol_name.append(para_setting_list_name)
        para_lol_value.append(para_setting_list_value)
        para_lol_name_with_value.append(para_setting_list_name_with_value)

    all_combination_list_name = [p for p in itertools.product(*para_lol_name)]
    all_combination_list_value = [p for p in itertools.product(*para_lol_value)]
    all_combination_list_name_with_value = [p for p in itertools.product(*para_lol_name_with_value)]
    all_combination_list_name_with_value_str = ['_'.join(i) for i in all_combination_list_name_with_value]

    para_dod = dict()
    element_index = 0
    for each_combination in all_combination_list_name_with_value_str:
        current_name_list   = all_combination_list_name[element_index]
        current_value_list  = all_combination_list_value[element_index]
        current_para_dict = dict()
        for key, value in zip(current_name_list, current_value_list):
            current_para_dict[key] = value
        para_dod[each_combination] = current_para_dict
        element_index += 1

    return para_dod


def fa2phy(fasta_in, phy_out):

    alignment = AlignIO.read(fasta_in, 'fasta')

    max_seq_id_len = 0
    for each_seq in alignment:
        seq_id_len = len(each_seq.id)
        if seq_id_len > max_seq_id_len:
            max_seq_id_len = seq_id_len

    with open(phy_out, 'w') as msa_out_handle:
        msa_out_handle.write('%s %s\n' % (len(alignment), alignment.get_alignment_length()))
        for each_seq in alignment:
            seq_id = each_seq.id
            seq_id_with_space = '%s%s' % (seq_id, ' ' * (max_seq_id_len + 2 - len(seq_id)))
            msa_out_handle.write('%s%s\n' % (seq_id_with_space, str(each_seq.seq)))


def dating(args):

    op_dir              = args['o']
    tree_file           = args['tree']
    msa_file            = args['msa']
    force_overwrite     = args['f']
    seq_type            = args['st']
    settings_to_compare = args['s']

    # out_group_txt           = args['og']
    # root_age                = args['ra']
    # para_to_test            = args['to_test']
    # js_cpu_num              = 1
    # quote_node_name         = False
    op_prefix = ''

    para_to_test_dict = dict()
    for each_para in open(settings_to_compare):
        each_para_split = each_para.strip().split()
        para_list = each_para_split[1].split(',')
        para_to_test_dict[each_para_split[0]] = para_list

    ####################################################################################################################

    tree_f_name, tree_f_path, tree_f_base, tree_f_ext = sep_path_basename_ext(tree_file)
    msa_f_name,  msa_f_path,  msa_f_base,  msa_f_ext  = sep_path_basename_ext(msa_file)

    get_bv_wd                           = '%s/get_bv_wd'                            % op_dir
    mcmctree_ctl_bv                     = '%s/mcmctree.ctl'                         % get_bv_wd
    mcmctree_cmds_txt                   = '%s/mcmctree_cmds.txt'                    % op_dir
    # tree_file_renamed                   = '%s/%s_renamed.treefile'                  % (op_dir, tree_f_base)
    # tree_file_rooted                    = '%s/%s_rooted.treefile'                   % (op_dir, tree_f_base)
    # tree_file_rooted_with_time          = '%s/%s_rooted_with_time.treefile'         % (op_dir, tree_f_base)
    # tree_file_rooted_with_time_final    = '%s/%s_rooted_with_time_final.treefile'   % (op_dir, tree_f_base)

    # create output folder
    if os.path.isdir(op_dir) is True:
        if force_overwrite is True:
            os.system('rm -r %s' % op_dir)
        else:
            print('Output folder exist, program exited!')
            exit()

    os.system('mkdir %s' % op_dir)

    ####################################################################################################################

    # prepare files for getting bv file
    os.system('mkdir %s'  % get_bv_wd)
    os.system('cp %s %s/' % (tree_file, get_bv_wd))
    os.system('cp %s %s/' % (msa_file, get_bv_wd))

    get_bv_para_dict = dict()
    get_bv_para_dict['seqfile']  = msa_f_name
    get_bv_para_dict['treefile'] = tree_f_name
    get_bv_para_dict['mcmcfile'] = 'mcmc.txt'
    get_bv_para_dict['outfile']  = 'out.txt'
    get_bv_para_dict['seqtype']  = seq_type
    get_bv_para_dict['usedata']  = '3'

    prep_mcmctree_ctl(get_bv_para_dict, mcmctree_ctl_bv)

    # write out command
    mcmctree_cmds_txt_handle = open(mcmctree_cmds_txt, 'w')
    mcmctree_cmds_txt_handle.write('cd %s; mcmctree\n' % get_bv_wd.split('/')[-1])
    mcmctree_cmds_txt_handle.write('\n# Please wait for the above command to be finished before you move to the following ones!\n\n')
    mcmctree_cmds_txt_handle.close()

    ####################################################################################################################

    para_comb_dict = get_parameter_combinations(para_to_test_dict)

    mcmctree_cmds_txt_handle = open(mcmctree_cmds_txt, 'a')
    for para_comb in sorted(list(para_comb_dict.keys())):

        # create dir
        current_dating_wd_1 = '%s/%s_run1'  % (op_dir, para_comb)
        current_dating_wd_2 = '%s/%s_run2'  % (op_dir, para_comb)
        os.system('mkdir %s' % current_dating_wd_1)
        os.system('mkdir %s' % current_dating_wd_2)

        # copy tree and msa file
        os.system('cp %s %s/' % (tree_file, current_dating_wd_1))
        os.system('cp %s %s/' % (tree_file, current_dating_wd_2))

        os.system('cp %s %s/' % (msa_file,  current_dating_wd_1))
        os.system('cp %s %s/' % (msa_file,  current_dating_wd_2))

        # prepare mcmctree.ctl file
        mcmctree_ctl_1  = '%s/mcmctree.ctl' % current_dating_wd_1
        mcmctree_ctl_2  = '%s/mcmctree.ctl' % current_dating_wd_2

        current_para_dict = para_comb_dict[para_comb]
        current_para_dict['seqfile']  = msa_f_name
        current_para_dict['treefile'] = tree_f_name
        current_para_dict['mcmcfile'] = '%s_mcmc.txt' % para_comb
        current_para_dict['outfile']  = '%s_out.txt'  % para_comb
        current_para_dict['seqtype']  = seq_type
        current_para_dict['usedata']  = '2'

        prep_mcmctree_ctl(current_para_dict, mcmctree_ctl_1)
        prep_mcmctree_ctl(current_para_dict, mcmctree_ctl_2)

        # write out commands
        mcmctree_cmds_txt_handle.write('cd %s; cp ../get_bv_wd/out.BV in.BV; mcmctree\n' % (current_dating_wd_1.split('/')[-1]))
        mcmctree_cmds_txt_handle.write('cd %s; cp ../get_bv_wd/out.BV in.BV; mcmctree\n' % (current_dating_wd_2.split('/')[-1]))
    mcmctree_cmds_txt_handle.close()

    print('Job script for performing dating exported to %s' % mcmctree_cmds_txt)

    ####################################################################################################################

    # # root genome tree with outgroup
    # root_with_out_group(tree_file_renamed, out_group_txt, tree_file_rooted)
    #
    # # remove "NoName" from the rooted tree with time constraints
    # tree_str = open(tree_file_rooted_with_time).readline().strip().replace('NoName', '')
    #
    # # add root age
    # tree_str = tree_str.replace(';', '<%s;' % root_age)
    # tre_object = Tree(tree_str, format=8, quoted_node_names=quote_node_name)
    # with open(tree_file_rooted_with_time_final, 'w') as tree_file_rooted_with_time_final_hanlde:
    #     tree_file_rooted_with_time_final_hanlde.write('%s\t1\n' % len(tre_object.get_leaf_names()))
    #     tree_file_rooted_with_time_final_hanlde.write(tree_str.replace('""', '') + '\n')
    #     #tree_file_rooted_with_time_final_hanlde.write(tree_str + '\n')
    #
    # # get BV file
    # os.mkdir(get_bv_wd)
    # os.system('cp %s %s/' % (msa_file, get_bv_wd))
    # os.system('cp %s %s/' % (tree_file_rooted_with_time_final, get_bv_wd))
    #
    # get_BV_js                       = '%s/get_BV.sh'            % (op_dir)
    # get_BV_mcmctree_ctl             = '%s_get_BV_mcmctree.ctl'  % (op_prefix)
    # pwd_get_BV_mcmctree_ctl         = '%s/%s'                   % (get_bv_wd, get_BV_mcmctree_ctl)
    #
    # get_BV_para_dict = dict()
    # get_BV_para_dict['seqfile']     = msa_file
    # get_BV_para_dict['treefile']    = tree_file_rooted_with_time_final
    # get_BV_para_dict['mcmcfile']    = '%s_mcmc.txt' % op_prefix
    # get_BV_para_dict['outfile']     = '%s_out.txt'  % op_prefix
    # get_BV_para_dict['seqtype']     = '2'
    # get_BV_para_dict['usedata']     = '3'
    # get_BV_para_dict['clock']       = '3'
    # prep_mcmctree_ctl(get_BV_para_dict, pwd_get_BV_mcmctree_ctl)
    #
    # with open(get_BV_js, 'w') as get_BV_js_handle:
    #     get_BV_js_handle.write('#!/bin/bash\n#SBATCH --ntasks 1\n#SBATCH --cpus-per-task %s\n\n' % js_cpu_num)
    #     get_BV_js_handle.write('cd %s/%s\n' % (os.getcwd(), get_bv_wd))
    #     get_BV_js_handle.write('mcmctree %s\n' % get_BV_mcmctree_ctl)
    #
    # # prepare files for dating
    # para_dod = get_parameter_combinations(para_to_test_dict)
    # for para_combination in para_dod:
    #     mcmctree_ctl         = '%s_%s_mcmctree.ctl'         % (op_prefix, para_combination)
    #     current_dating_wd    = '%s/%s_DeltaLL_%s_dating_wd' % (op_dir, op_prefix.split('_DeltaLL_stdout')[0], para_combination)
    #     pwd_mcmctree_ctl     = '%s/%s_%s_mcmctree.ctl'      % (current_dating_wd, op_prefix, para_combination)
    #     js_mcmctree          = '%s/js_%s_DeltaLL_%s.sh'     % (op_dir, op_prefix.split('_DeltaLL_stdout')[0], para_combination)
    #     pwd_aln_in_dating_wd = '%s/%s'                      % (current_dating_wd, msa_file)
    #
    #     # create dating wd and copy tree and alignment files into it
    #     os.mkdir(current_dating_wd)
    #     os.system('cp %s %s/' % (tree_file_rooted_with_time_final, current_dating_wd))
    #
    #     current_para_dict = para_dod[para_combination]
    #     current_para_dict['seqfile']  = msa_file
    #     current_para_dict['treefile'] = tree_file_rooted_with_time_final
    #     current_para_dict['mcmcfile'] = '%s_%s_mcmc.txt' % (op_prefix, para_combination)
    #     current_para_dict['outfile']  = '%s_%s_out.txt'  % (op_prefix, para_combination)
    #     current_para_dict['seqtype']  = '2'
    #     current_para_dict['usedata']  = '2'
    #
    #     prep_mcmctree_ctl(current_para_dict, pwd_mcmctree_ctl)
    #
    #     with open(js_mcmctree, 'w') as js_mcmctree_handle:
    #         js_mcmctree_handle.write('#!/bin/bash\n\n')
    #         js_mcmctree_handle.write('cd %s/%s\n' % (os.getcwd(), current_dating_wd))
    #         js_mcmctree_handle.write('cp ../%s_get_BV_wd/out.BV in.BV\n' % op_prefix)
    #         js_mcmctree_handle.write('mcmctree %s\n' % mcmctree_ctl)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-tree',    required=True,                          help='outgroup leaves, one id per line')
    parser.add_argument('-msa',     required=True,                          help='EU tree with time constraints')
    parser.add_argument('-o',       required=True,                          help='dating wd')
    parser.add_argument('-s',       required=True,                          help='settings to compare')
    parser.add_argument('-st',      required=False, default='2',            help='sequence type, 0 for nucleotides, 1 for codons, 2 for AAs, default: 2')
    parser.add_argument('-f',       required=False, action="store_true",    help='force overwrite')
    args = vars(parser.parse_args())
    dating(args)


'''

cd /Users/songweizhi/Desktop/dating_test
/usr/local/bin/python3.7 /Users/songweizhi/PycharmProjects/TreeSAK/TreeSAK/dating.py -tree tree.txt -msa marker_gene.phylip -o dating_wd -f

cd /Users/songweizhi/Desktop/mcmctree.example
/usr/local/bin/python3.7 /Users/songweizhi/PycharmProjects/TreeSAK/TreeSAK/dating.py -tree Chi23.tree -msa 12tr_Chi23.phy -o 12tr_dating_wd -f

python3 dating.py -tree Chi23.tree -msa 12tr/12tr_Chi23.phy -o 12tr_dating_wd -f -s settings_to_compare.txt

'''
