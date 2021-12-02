import XCTest
import class Foundation.Bundle
@testable import HW3Lib

final class HW3Tests: XCTestCase {
    func testConstructor() {
        var sport = SportCar(nil, nil, nil, nil, nil, nil)
        XCTAssertEqual(true, sport == SportCar())

        sport = SportCar(nil, 1993, nil, nil, true, nil)
        XCTAssertEqual(true, sport == SportCar("Custom", 1993, 0, 0, true, false))

        var trunk = TrunkCar(nil, nil, nil, nil, nil, nil)
        XCTAssertEqual(true, trunk == TrunkCar())

        trunk = TrunkCar(nil, 2001, nil, nil, true, nil)
        XCTAssertEqual(true, trunk == TrunkCar("Custom", 2001, 0, 0, true, false))
    }

    func testToString() {
        var sport = SportCar()
        var trunk = TrunkCar()
        var expected = """
                       Brand: Custom
                       Year: not stated
                       Trunk: 0/0
                       Is engine running: false
                       Are the windows open: false
                       """
        XCTAssertEqual(expected, sport.ToString())
        XCTAssertEqual(expected, trunk.ToString())

        sport = SportCar("Shevrolet", 2022, 10, 0, true, false)
        expected = """
                   Brand: Shevrolet
                   Year: 2022
                   Trunk: 0/10
                   Is engine running: true
                   Are the windows open: false
                   """
        XCTAssertEqual(expected, sport.ToString())
    }

    func testChangeState() {
        var sport = SportCar("Shevrolet", 2022, 10, 0, true, false)
        var a = Action.changeWindowsState(state: true)
        sport.ChangeState(a)
        XCTAssertEqual(true, sport == SportCar("Shevrolet", 2022, 10, 0, true, true))

        a = Action.changeEngineState(state: false)
        sport.ChangeState(a)
        XCTAssertEqual(true, sport == SportCar("Shevrolet", 2022, 10, 0, false, true))
        XCTAssertEqual(false, sport == SportCar("Shevrolett", 2022, 10, 0, false, true))
        XCTAssertEqual(false, sport == SportCar("Shevrolet", 2020, 10, 0, false, true))

        a = Action.changeTrunk(isPutting: true, amount: 5)
        sport.ChangeState(a)
        XCTAssertEqual(true, sport == SportCar("Shevrolet", 2022, 10, 5, false, true))

        a = Action.changeTrunk(isPutting: false, amount: 3)
        sport.ChangeState(a)
        XCTAssertEqual(true, sport == SportCar("Shevrolet", 2022, 10, 2, false, true))

        a = Action.changeTrunk(isPutting: false, amount: 20)
        XCTAssert(!sport.ChangeState(a))
    }

    static var allTests = [
        ("testConstructor", testConstructor),
        ("testToString", testToString),
        ("testChangeState", testChangeState),
    ]
}