class TestEvaluateModel(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.trainer = IntentClassifierTrainer()
        self.trainer.model = Mock()
        
        # Sample test data
        self.X_test = np.array([[1, 2], [3, 4], [5, 6]])
        self.y_test = np.array([0, 1, 2])
        self.label_classes = ['Class_A', 'Class_B', 'Class_C']
        
    @patch('simple_ml_trainer.classification_report')
    @patch('simple_ml_trainer.f1_score')
    @patch('simple_ml_trainer.accuracy_score')
    @patch('builtins.print')
    def test_evaluate_model_perfect_predictions(self, mock_print, mock_accuracy, mock_f1, mock_report):
        """Test evaluate_model with perfect predictions"""
        # Setup mock returns
        test_pred = np.array([0, 1, 2])
        self.trainer.model.predict.return_value = test_pred
        
        mock_accuracy.return_value = 1.0
        mock_f1.side_effect = [1.0, 1.0]  # weighted, macro
        mock_report.side_effect = [
            "Perfect Report",
            {'Class_A': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0}}
        ]
        
        # Execute
        result = self.trainer.evaluate_model(self.X_test, self.y_test, self.label_classes)
        
        # Verify model.predict was called correctly
        self.trainer.model.predict.assert_called_once()
        np.testing.assert_array_equal(
            self.trainer.model.predict.call_args[0][0], 
            self.X_test
        )
        
        # Verify sklearn functions called correctly
        mock_accuracy.assert_called_once_with(self.y_test, test_pred)
        self.assertEqual(mock_f1.call_count, 2)
        mock_f1.assert_any_call(self.y_test, test_pred, average='weighted')
        mock_f1.assert_any_call(self.y_test, test_pred, average='macro')
        
        # Verify classification_report called twice (print and dict)
        self.assertEqual(mock_report.call_count, 2)
        mock_report.assert_any_call(
            self.y_test, test_pred, 
            target_names=self.label_classes,
            digits=4
        )
        mock_report.assert_any_call(
            self.y_test, test_pred,
            target_names=self.label_classes,
            output_dict=True
        )
        