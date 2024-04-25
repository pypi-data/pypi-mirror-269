@pytest.mark.parametrize("kws,ans", [
    pytest.param({}, [3, {3: "(auto)"}, [[1, 2, 3]], {"1_((1,), (1,))": ("hf", "psi4")}]),
    pytest.param({"levels": {3: "p4-mp2-dz"}}, [3, {3: "p4-mp2-dz"}, [[1, 2, 3]], {"1_((3,), (3,))": ("mp2", "psi4")} ]),
    pytest.param({"levels": {1: "p4-mp2-dz", 3: "c4-ccsd-tz"}}, [3, {1: "p4-mp2-dz", 3: "c4-ccsd-tz"}, [[1], [2, 3]], {"1_((1,), (1,))": ("mp2", "psi4"), "2_((1, 2, 3), (1, 2, 3))": ("ccsd", "cfour")} ]),
])
def test_mbe_multilevel(mbe_data_multilevel, kws, ans):
    mbe_data_multilevel["specification"]["keywords"] = kws

    input_model = ManyBodyInput(**mbe_data_multilevel)
    comp_model = ManyBodyComputerQCNG.from_qcschema(input_model, build_tasks=True)

    assert comp_model.nfragments == 3
    assert comp_model.max_nbody == ans[0]
    assert list(comp_model.levels.items()) == list(ans[1].items())  # compare as OrderedDict
    assert comp_model.nbodies_per_mc_level == ans[2]

    import pprint
    pprint.pprint(comp_model.model_dump(), width=200)

    for k, v in ans[3].items():
        assert comp_model.task_list[k].method == v[0]
        assert comp_model.task_list[k].program == v[1]



