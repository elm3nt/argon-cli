VN = 1

ALL_DIRS = 1
RENDUNDANT_DIRS = 2

DATA = 'D'
ABSTRACT = 'A'
CONTROL_FLOW = 'C'
VIRTUALIZATION = 'V'

OBFUSCATION = {
    'abstract': 'tigress \
		--Verbosity=1 \
		--FilePrefix=v{vn}a \
		--Transform=Split \
		--Seed=0 \
		--SplitKinds=deep,block,top \
		--SplitCount=10 \
		--Functions=SECRET \
		--Transform=CleanUp \
		--CleanUpKinds=annotations \
		--out={output} {input}',

	'abstract-2': '''tigress \
		--FilePrefix=v{vn}b \
		--Verbosity=1  \
		--Transform=RndArgs \
		--Seed=0 \
		--RndArgsBogusNo=2?5 \
				''' + "--Functions=_v{vn}a_1_SECRET_SECRET_split_1"
				+ ",_v{vn}a_1_SECRET_SECRET_split_2"
				+ ",_v{vn}a_1_SECRET_SECRET_split_3"
				+ ",_v{vn}a_1_SECRET_SECRET_split_4"
				+ ",_v{vn}a_1_SECRET_SECRET_split_5"
				+ ",_v{vn}a_1_SECRET_SECRET_split_6"
				+ ",_v{vn}a_1_SECRET_SECRET_split_7"
				+ ",_v{vn}a_1_SECRET_SECRET_split_8"
				+ ",_v{vn}a_1_SECRET_SECRET_split_9"
				+ ",_v{vn}a_1_SECRET_SECRET_split_10 " +
'''--Transform=CleanUp \
		--CleanUpKinds=annotations \
		--out={output} {input}''',

	'abstract-3': '''tigress --Verbosity=1   \
		--FilePrefix=v{vn} \
		--Transform=InitEntropy \
		--Functions=main  \
		--Transform=InitOpaque \
		--Functions=main \
		--InitOpaqueCount=2 \
		--InitOpaqueStructs=list,array  \
				--Transform=Merge \
				''' + "--Functions=_v{vn}a_1_SECRET_SECRET_split_1"
				+ ",_v{vn}a_1_SECRET_SECRET_split_2"
				+ ",_v{vn}a_1_SECRET_SECRET_split_3"
				+ ",_v{vn}a_1_SECRET_SECRET_split_4"
				+ ",_v{vn}a_1_SECRET_SECRET_split_5"
				+ ",_v{vn}a_1_SECRET_SECRET_split_6"
				+ ",_v{vn}a_1_SECRET_SECRET_split_7"
				+ ",_v{vn}a_1_SECRET_SECRET_split_8"
				+ ",_v{vn}a_1_SECRET_SECRET_split_9"
				+ ",_v{vn}a_1_SECRET_SECRET_split_10 " +
		'''--Transform=CleanUp \
		--CleanUpKinds=annotations \
		--out={output} {input}''',

	'control-flow': 'tigress \
		--Verbosity=1 \
		--FilePrefix=v{vn} \
		--Transform=InitOpaque \
		--Functions=main \
		--Transform=UpdateOpaque \
		--Functions=SECRET \
		--UpdateOpaqueCount=10 \
		--Transform=AddOpaque \
		--Functions=SECRET \
		--AddOpaqueCount=10  \
		--AddOpaqueKinds=call,bug,true,junk \
		--Transform=Flatten \
		--Functions=SECRET \
		-FlattenObfuscateNext=true \
		--FlattenDispatch=switch \
		--Transform=CleanUp \
		--CleanUpKinds=annotations \
		--out={output} {input}',

	'data': 'tigress \
		--Verbosity=1  \
		--FilePrefix=v{vn} \
		--Transform=InitEntropy \
		--Functions=main  \
		--Transform=EncodeLiterals \
		--Functions=SECRET  \
		--Transform=CleanUp \
		--CleanUpKinds=annotations \
		--out={output} {input}',

	'virtualization': 'tigress \
		--Verbosity=1  \
		--FilePrefix=v{vn} \
		--Transform=Virtualize \
		--Functions=SECRET \
		--VirtualizeDispatch=switch \
		--Transform=CleanUp \
		--CleanUpKinds=annotations \
		--out={output} {input}'
	}
