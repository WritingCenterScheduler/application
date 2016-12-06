# import unittest
# import numpy as np
# from app.engine import models
# import sampledata
# from app import models, config
# from mongoengine import *
#
# class TestDBConnect(unittest.TestCase):
#
#     def setUp(self):
#
#         # Create Test Employee
#         self.tc1 = "010"
#         self.candidate1 = models.Employee(sampledata.e1av, typecode=self.tc1, pid=1)
#         self.candidate2 = models.Employee(sampledata.e2av, typecode=self.tc1, pid=2)
#         self.candidate3 = models.Employee(sampledata.e3av, typecode=self.tc1, pid=3)
#         self.candidate4 = models.Employee(sampledata.e4av, typecode=self.tc1, pid=4)
#         # Create Test Location
#         self.location1 = models.Location()
#         self.location1.timeslots = sampledata.loc1
#
#         # Add employee to location and location to schedule manager
#         self.location1.add_possible_candidate(self.candidate1)
#         self.location1.add_possible_candidate(self.candidate2)
#         self.location1.add_possible_candidate(self.candidate3)
#         self.location1.add_possible_candidate(self.candidate4)
#         self.sm.add_location(self.location1)
#
#     def tearDown(self):
#         del self.sm
#         del self.candidate1
#         del self.candidate2
#         del self.candidate3
#         del self.candidate4
#         del self.location1
#         del self.tc1
#         try:
#             while(True):
#                 u = db_models.User.objects.first()
#                 u.delete()
#         except:
#             return "Done"
#
#     def test_make(self):
#         self.assertTrue(isinstance(self.sm, models.ScheduleManager))
#
#     def test_calculate_need(self):
#         """
#         Tests the population of a Location object's need array, which contains
#         the weighted "need" value of each timeslot. The weighted "need" value of
#         a timeslot denotes the priority that it will be given while scheduling.
#         """
#
#         # Call the calculate_need() function for a location in schedule_manager
#         # This should populate the need array for the Location object
#         self.location1.calculate_need()
#         self.assertIsNotNone(self.location1.need)
#
#     def test_initialize_location_schedule(self):
#         """
#         Tests the initialization of the dimensions of the Location object's
#         schedule array.
#         """
#
#         # Call the initialize_dimensions() function for the location
#         # This should initialize the dimensions of the schedule to match the
#         # dimensions of the timeslot requirements
#         width = len(self.sm.locations[0].timeslots[0]["requirements"])
#         height = len(self.sm.locations[0].timeslots[0]["requirements"][0])
#         self.sm.locations[0].initialize_dimensions(width, height, 2)
#
#         self.assertEqual(len(self.sm.locations[0].schedule), width)
#         self.assertEqual(len(self.sm.locations[0].schedule[0]), height)
#         self.assertEqual(len(self.sm.locations[0].schedule[0][0]), 2)
#
#     def test_insert_users_basic(self):
#         """
#         Basic test for inserting users into the database
#         """
#         for i in range(4):
#             u = db_models.User()
#             u.init(pid=i)
#             u.save()
#         # print (db_models.User.objects.to_json())
#         # print (len(db_models.User.objects))
#         self.assertTrue(len(db_models.User.objects) is 4)
#
#     def test_insert_users(self):
#         """
#         Test for creating users with unique availabilities and checking persistence.
#         """
#         for c in self.location1.possible_candidates:
#             u_avail = db_config.DEFAULT_AVAILABILITY
#             for k in u_avail:
#                 for i in range(len(c.availability)):
#                     if k == 'sun':
#                         u_avail[k][i] = str(c.availability[i][0])
#                     elif k == 'mon':
#                         u_avail[k][i] = str(c.availability[i][1])
#                     elif k == 'tue':
#                         u_avail[k][i] = str(c.availability[i][2])
#                     elif k == 'wed':
#                         u_avail[k][i] = str(c.availability[i][3])
#                     elif k == 'thu':
#                         u_avail[k][i] = str(c.availability[i][4])
#                     elif k == 'fri':
#                         u_avail[k][i] = str(c.availability[i][5])
#                     else:
#                         u_avail[k][i] = str(c.availability[i][6])
#             u = db_models.User()
#             u.init(pid = c.pid, availability=u_avail)
#             u.save()
#         self.assertEqual(len(db_models.User.objects), len(self.location1.possible_candidates))
#
#     def test_insert_and_run(self):
#         """
#         Tests pulling employee availability from database and running scheduler,
#         then putting the resulting schedule back into the database
#         """
#         for c in self.location1.possible_candidates:
#             u_avail = db_config.DEFAULT_AVAILABILITY
#             for k in u_avail:
#                 for i in range(len(c.availability)):
#                     if k == 'sun':
#                         u_avail[k][i] = str(c.availability[i][0])
#                     elif k == 'mon':
#                         u_avail[k][i] = str(c.availability[i][1])
#                     elif k == 'tue':
#                         u_avail[k][i] = str(c.availability[i][2])
#                     elif k == 'wed':
#                         u_avail[k][i] = str(c.availability[i][3])
#                     elif k == 'thu':
#                         u_avail[k][i] = str(c.availability[i][4])
#                     elif k == 'fri':
#                         u_avail[k][i] = str(c.availability[i][5])
#                     else:
#                         u_avail[k][i] = str(c.availability[i][6])
#             u = db_models.User()
#             u.init(pid = c.pid, typecode=c.typecode, availability=u_avail)
#             u.save()
#
#         # Create Test Employee
#         self.candidates = []
#         for u in db_models.User.objects:
#             av = np.zeros((8,7))
#             # print (av)
#             for k in u.availability:
#                 for i in range(len(u.availability[k])):
#                     if k == 'sun':
#                         av[i][0] = int(u.availability[k][i])
#                     elif k == 'mon':
#                         av[i][1] = int(u.availability[k][i])
#                     elif k == 'tue':
#                         av[i][2] = int(u.availability[k][i])
#                     elif k == 'wed':
#                         av[i][3] = int(u.availability[k][i])
#                     elif k == 'thu':
#                         av[i][4] = int(u.availability[k][i])
#                     elif k == 'fri':
#                         av[i][5] = int(u.availability[k][i])
#                     else:
#                         av[i][6] = int(u.availability[k][i])
#             print (u.availability)
#             print (av)
#             c = models.Employee(av, typecode=u.typecode, pid=u.pid)
#             self.candidates.append(c)
#         self.tc1 = self.candidates[0].typecode
#         self.candidate1 = self.candidates[0]
#         self.candidate2 = self.candidates[1]
#         self.candidate3 = self.candidates[2]
#         self.candidate4 = self.candidates[3]
#         # Create Test Location
#         self.location1 = models.Location()
#         self.location1.timeslots = sampledata.loc1
#
#         # Add employee to location and location to schedule manager
#         self.location1.add_possible_candidate(self.candidate1)
#         self.location1.add_possible_candidate(self.candidate2)
#         self.location1.add_possible_candidate(self.candidate3)
#         self.location1.add_possible_candidate(self.candidate4)
#         self.sm.add_location(self.location1)
#
#         # Does the actual scheduling
#         # The following code is the same as the code from testrun.py
#         for c in self.sm.locations[0].possible_candidates:
#             print (c.pid)
#
#         self.assertTrue(True)
#
# if __name__ == "__main__":
#     unittest.main()
