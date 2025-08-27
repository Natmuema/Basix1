import React, { useState, useEffect } from "react";
import { X, PlusCircle, Trash2, Bell, AlertCircle } from "lucide-react";

const InvestmentAlertsModal = ({ isOpen, onClose }) => {
  const [alerts, setAlerts] = useState([]);
  const [newAlert, setNewAlert] = useState({
    type: "price_increase",
    asset: "",
    condition: "",
    value: "",
  });

  // Load alerts from localStorage on mount
  useEffect(() => {
    const storedAlerts = localStorage.getItem("investmentAlerts");
    if (storedAlerts) {
      setAlerts(JSON.parse(storedAlerts));
    }
  }, []);

  // Save alerts to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem("investmentAlerts", JSON.stringify(alerts));
  }, [alerts]);

  // Close modal if not open
  if (!isOpen) return null;

  const handleAddAlert = () => {
    if (!newAlert.asset || !newAlert.value) return;
    setAlerts([...alerts, newAlert]);
    setNewAlert({ type: "price_increase", asset: "", condition: "", value: "" });
  };

  const handleDeleteAlert = (index) => {
    setAlerts(alerts.filter((_, i) => i !== index));
  };

  const toggleAlert = (index) => {
    setAlerts(
      alerts.map((alert, i) =>
        i === index ? { ...alert, active: !alert.active } : alert
      )
    );
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" id='investment-alerts'>
      <div className="bg-white rounded-2xl w-full max-w-lg shadow-xl">
        {/* Header */}
        <div className="flex justify-between items-center p-4 border-b">
          <h2 className="text-xl font-semibold flex items-center">
            <Bell className="w-5 h-5 mr-2 text-cyan-600" />
            Investment Alerts
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Alerts List */}
        <div className="p-4 max-h-96 overflow-y-auto">
          {alerts.length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              <AlertCircle className="w-10 h-10 mx-auto mb-2 text-gray-400" />
              <p>No alerts set yet. Add one below.</p>
            </div>
          ) : (
            alerts.map((alert, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 mb-2 bg-gray-50 rounded-lg"
              >
                <div>
                  <p className="font-medium">
                    {alert.asset} - {alert.type.replace("_", " ")}
                  </p>
                  <p className="text-sm text-gray-500">
                    {alert.value} {alert.condition && `(${alert.condition})`}
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => toggleAlert(index)}
                    className={`px-2 py-1 rounded text-xs ${
                      alert.active
                        ? "bg-green-100 text-green-600"
                        : "bg-gray-200 text-gray-500"
                    }`}
                  >
                    {alert.active ? "Active" : "Inactive"}
                  </button>
                  <button
                    onClick={() => handleDeleteAlert(index)}
                    className="text-red-500 hover:text-red-700"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Add Alert Form */}
        <div className="p-4 border-t">
          <div className="space-y-3">
            <select
              className="w-full p-2 border rounded-lg"
              value={newAlert.type}
              onChange={(e) =>
                setNewAlert({ ...newAlert, type: e.target.value })
              }
            >
              <option value="price_increase">Price Increase</option>
              <option value="price_drop">Price Drop</option>
              <option value="volume_spike">Volume Spike</option>
              <option value="risk_change">Risk Level Change</option>
            </select>
            <input
              type="text"
              placeholder="Asset name"
              className="w-full p-2 border rounded-lg"
              value={newAlert.asset}
              onChange={(e) =>
                setNewAlert({ ...newAlert, asset: e.target.value })
              }
            />
            <input
              type="number"
              placeholder="Value"
              className="w-full p-2 border rounded-lg"
              value={newAlert.value}
              onChange={(e) =>
                setNewAlert({ ...newAlert, value: e.target.value })
              }
            />
            <button
              onClick={handleAddAlert}
              className="w-full bg-cyan-600 text-white py-2 rounded-lg flex items-center justify-center hover:bg-cyan-700"
            >
              <PlusCircle className="w-5 h-5 mr-2" />
              Add Alert
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InvestmentAlertsModal;

