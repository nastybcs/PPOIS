
import unittest

from transport.route import Route
from transport.route_point import RoutePoint
from enums.route_status import RouteStatus
from exceptions.errors import DeliveryError
from storage.warehouse_module import Warehouse
from staff.department import HRDepartment


class TestRoute(unittest.TestCase):

    def setUp(self):
    

        warehouse = Warehouse("Test Warehouse")
        hr = HRDepartment(warehouse)
        self.driver = hr.hire_driver("Ivan", "Petrov", "Moscow", "ivan@petrov", "A123BC")

        self.vehicle = "A123BC"
        self.route = Route(self.driver, self.vehicle)


    def test_init_sets_id_and_status(self):
        self.assertGreater(self.route.route_id, 0)
        self.assertEqual(self.route.driver, self.driver)
        self.assertEqual(self.route.vehicle, self.vehicle)
        self.assertEqual(self.route.points, [])
        self.assertEqual(self.route.status, RouteStatus.PLANNED)
        self.assertIsNone(self.route.started_at)
        self.assertIsNone(self.route.completed_at)

    def test_id_counter_increments(self):
        route2 = Route(self.driver, self.vehicle)
        self.assertEqual(route2.route_id, self.route.route_id + 1)


    def test_add_point_success_in_planned(self):
        point = RoutePoint("Moscow, Lenina 10")
        self.route.add_point(point)
        self.assertIn(point, self.route.points)

    def test_add_point_raises_if_not_planned(self):
        point = RoutePoint("SPb")
        self.route.add_point(point)
        self.route.start()
        with self.assertRaises(DeliveryError) as cm:
            self.route.add_point(RoutePoint("Kazan"))
        self.assertIn("после начала", str(cm.exception))


    def test_start_success_with_points(self):
        point = RoutePoint("Moscow")
        self.route.add_point(point)
        self.route.start()
        self.assertEqual(self.route.status, RouteStatus.IN_PROGRESS)
        self.assertIsNotNone(self.route.started_at)

    def test_start_raises_if_no_points(self):
        with self.assertRaises(DeliveryError) as cm:
            self.route.start()
        self.assertIn("без точек", str(cm.exception))

    def test_start_raises_if_not_planned(self):
        point = RoutePoint("Moscow")
        self.route.add_point(point)
        self.route.start()
        with self.assertRaises(DeliveryError) as cm:
            self.route.start()
        self.assertIn("уже начат", str(cm.exception))

    def test_mark_point_visited_success(self):
        point = RoutePoint("Moscow")
        self.route.add_point(point)
        self.route.start()
        self.route.mark_point_visited(0)
        self.assertTrue(point.visited)
        self.assertIsNotNone(point.arrival_time)

    def test_mark_point_visited_raises_if_not_in_progress(self):
        point = RoutePoint("Moscow")
        self.route.add_point(point)
        with self.assertRaises(DeliveryError) as cm:
            self.route.mark_point_visited(0)
        self.assertIn("не находится в пути", str(cm.exception))


    def test_complete_success_when_all_visited(self):
        point = RoutePoint("Moscow")
        self.route.add_point(point)
        self.route.start()
        self.route.mark_point_visited(0)
        self.route.complete()
        self.assertEqual(self.route.status, RouteStatus.COMPLETED)
        self.assertIsNotNone(self.route.completed_at)

    def test_complete_raises_if_not_all_visited(self):
        point1 = RoutePoint("Moscow")
        point2 = RoutePoint("SPb")
        self.route.add_point(point1)
        self.route.add_point(point2)
        self.route.start()
        self.route.mark_point_visited(0)
        with self.assertRaises(DeliveryError) as cm:
            self.route.complete()
        self.assertIn("Не все точки", str(cm.exception))

    def test_complete_raises_if_not_in_progress(self):
        with self.assertRaises(DeliveryError) as cm:
            self.route.complete()
        self.assertIn("неактивный", str(cm.exception))


    def test_cancel_success_in_planned(self):
        self.route.cancel()
        self.assertEqual(self.route.status, RouteStatus.CANCELLED)

    def test_cancel_success_in_progress(self):
        point = RoutePoint("Moscow")
        self.route.add_point(point)
        self.route.start()
        self.route.cancel()
        self.assertEqual(self.route.status, RouteStatus.CANCELLED)

    def test_cancel_raises_if_completed(self):
        point = RoutePoint("Moscow")
        self.route.add_point(point)
        self.route.start()
        self.route.mark_point_visited(0)
        self.route.complete()
        with self.assertRaises(DeliveryError) as cm:
            self.route.cancel()
        self.assertIn("завершённый", str(cm.exception))

    def test_info_returns_correct_structure(self):
        point = RoutePoint("Moscow, Lenina 10", "Склад")
        self.route.add_point(point)
        self.route.start()
        self.route.mark_point_visited(0)

        info = self.route.info()
        self.assertEqual(info["route_id"], self.route.route_id)
        self.assertEqual(info["driver"], "Ivan Petrov")
        self.assertEqual(info["vehicle"], "A123BC")
        self.assertEqual(info["points_total"], 1)
        self.assertEqual(info["visited"], 1)
        self.assertEqual(info["status"], RouteStatus.IN_PROGRESS.value)
