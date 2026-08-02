const mongoose = require('mongoose');

const orderSchema = new mongoose.Schema({
  title:       { type: String, required: true },
  description: { type: String, default: '' },
  status:      { type: String, enum: ['pending', 'in-progress', 'done'], default: 'pending' },
  userId:      { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  createdAt:   { type: Date, default: Date.now }
});

module.exports = mongoose.model('Order', orderSchema);
