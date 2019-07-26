VN = 1
DATA = 'D'
ABSTRACT = 'A'
CONTROL_FLOW = 'C'
VIRTUALIZATION = 'V'

NL = repr('\\n').replace('\'', '')

TIGRESS_REGREX = {
    'pass': '  char password{count}[100] = "";',
    'printf': '  printf("Please enter password:");\n  ' +
                'scanf("%s", password{count});',
    'check_pass': '  stringCompareResult = strncmp(password{count}, "{password}", 100UL);\n  ' +
                'failed |= stringCompareResult != 0UL;',

    'code': '  int activationCode{count} ;',
    'input': '  activationCode{count} = input[0UL];',
    'check_code': '  failed |= activationCode{count} != {code}UL;',

    'randfuns': '    randomFuns_value6 = strtoul(argv[randomFuns_i5 + {index}], 0, 10);\n    ' +
                'input[randomFuns_i5 + {index2}] = randomFuns_value6;',

    'megaint': 'argc != {count} ) {{\n    ' +
               'printf("Call this program with %i arguments ' + NL + '", {count2});'
}

TIGRESS_CMD = {
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
        --out={output} {input}',

    'generate': 'tigress \
        --Verbosity=1 \
        --Seed=0 \
        --Transform=RandomFuns \
        --RandomFunsName=SECRET \
        --RandomFunsType=long \
        --RandomFunsInputSize=1 \
        --RandomFunsStateSize=1 \
        --RandomFunsOutputSize=1 \
        --RandomFunsCodeSize=10 \
        {option} \
        --RandomFunsFailureKind=segv  \
        --out={output} {input}',

    'code': '--RandomFunsActivationCodeCheckCount=1 \
             --RandomFunsActivationCode={code}',

    'pass': '--RandomFunsPasswordCheckCount=1 \
             --RandomFunsPassword={password}'
}
