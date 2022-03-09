import DE_Homework_Mikko_Hirvola as hw

import sys

if(len(sys.argv)>=2):
    if(sys.argv[1] == "prepare"):
        print("\nPreparing SQLite database")
        hw.prepare()
    if(sys.argv[1] == "task1"):
        print("\nStarting task 1")
        hw.task_1()
    if(sys.argv[1] == "task2"):
        print("\nStarting task 2, in case there is no assert errors, everything went through. These can also be executed via pytest DE_Homework_Mikko_Hirvola.py after running preparation")
        hw.test_task_2_a()
        hw.test_task_2_b()
        hw.test_task_2_c()
    if(sys.argv[1] == "task3"):
        print("\nStarting task 3")
        hw.task_3()
    if(sys.argv[1] == "task4"):
        print("\nStarting task 4")
        hw.task_4()
    if(sys.argv[1] == "task5"):
        print("\nStarting task 5")
        hw.task_5()
    if(sys.argv[1] == "taskbonus"):
        print("\nStarting bonus task")
        hw.task_bonus()
    if(sys.argv[1] == "clean"):
        print("\nResetting folder to starting state")
        hw.clean()

else:
    print("""\nUsage: python main.py [prepare|task1|task2|task3|task4|task5|taskbonus|clean]
Prepare should be executed before running any tasks.
Task commands will each run their respective tasks.
Clean will remove all files created by preparation or any task.\n""")




