import argparse

ag = argparse.ArgumentParser()
ag.add_argument('-i', '--dataset', help='path to input directory of images')
args = ag.parse_args()
print(args)
if args.dataset:
	print('True')
