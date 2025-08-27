import React from 'react'

const Footer = () => {
  return (
    <div className=" text-white py-6">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center">
          <div className="text-sm">
            &copy; {new Date().getFullYear()} BASIX IP Marketplace. All rights reserved.
          </div>
          <div className="space-x-4">
            <a href="/privacy" className="text-sm hover:underline">Privacy Policy</a>
            <a href="/terms" className="text-sm hover:underline">Terms of Service</a>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Footer