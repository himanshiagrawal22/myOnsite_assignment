from app.prediction import predict_population


def test_population_prediction():

    features = {
        "average_masked_mean": 45.5,
        "average_masked_max": 80.0,
        "average_masked_min": 10.0,
        "average_masked_stdDev": 15.0,
        "Brightness_Range": 70.0,
        "Brightness_Ratio": 1.7582,
        "Brightness_Product": 3640.0
    }

    result = predict_population(features)

    assert "estimated_population" in result
    assert "features_used" in result

    assert isinstance(
        result["estimated_population"],
        int
    )

    assert len(result["features_used"]) == 7