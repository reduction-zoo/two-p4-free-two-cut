from check import legal_source, solve_source, valid_source, legal_target, solve_target, valid_target


def test_hand_cases():
    k4 = {"vertices":4,"edges":[[u,v] for u in range(4) for v in range(u+1,4)]}
    assert valid_source(k4,{"side":[False,False,True,True]})
    assert "side" in solve_target(k4)
    k5 = {"vertices":5,"edges":[[u,v] for u in range(5) for v in range(u+1,5)]}
    assert solve_source(k5) == {"status":"NO-SOLUTION"}
    paths = {"vertices":9,"edges":[[0,1],[1,2],[2,3],[4,5],[5,6],[6,7],[0,8],[4,8]]}
    assert not legal_target(paths)
    path8 = {"vertices":8,"edges":[[i,i+1] for i in range(7)]}
    assert legal_target(path8)
    assert not legal_source({"vertices":2,"edges":[]})
    assert not valid_target(k4,{"side":[False]*4})


if __name__ == "__main__":
    test_hand_cases()
