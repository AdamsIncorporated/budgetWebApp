// TableComponent.tsx
import React, { useState, useEffect, useRef, useMemo } from "react";
import { AgGridReact } from "@ag-grid-community/react";
import { BsDownload, BsArrowClockwise } from "react-icons/bs";
import { LoadingOverlay } from "../../components/loading/LoaderOverlay";
import "@ag-grid-community/styles/ag-grid.css";
import "@ag-grid-community/styles/ag-theme-quartz.css";
import { ClientSideRowModelModule } from "@ag-grid-community/client-side-row-model";
import { CsvExportModule } from "@ag-grid-community/csv-export";
import { ModuleRegistry } from "@ag-grid-community/core";

ModuleRegistry.registerModules([ClientSideRowModelModule, CsvExportModule]);

// Define the type of vendor data you expect to receive
interface Vendor {
  Id: number;
  FiscalYear: string;
  VendorName: string;
  InvoiceNumber: number;
  Amount: number;
  CheckDate: string;
  CheckNumber: number;
  DateCashed: Date;
  VoucherStatus: string;
  PostingStatus: string;
}

export default function BudgetPage() {
  const [vendors, setVendors] = useState<Vendor[]>([]);
  const [loading, setLoading] = useState<boolean>(false);  // Add loading state
  const gridRef = useRef<AgGridReact | null>(null);

  useEffect(() => {
    fetchVendors();
  }, []);

  const fetchVendors = async () => {
    setLoading(true);  // Start loading
    try {
      const response = await fetch("/api/vendors");
      if (!response.ok) {
        throw new Error("Failed to fetch vendor data");
      }
      const data = await response.json();
      setVendors(data);  // Update state with fetched vendor data
    } catch (error) {
      console.error("Error fetching vendor data:", error);
    } finally {
      setLoading(false);  // End loading
    }
  };

  const columnDefs = useMemo(
    () => [
      { field: "FiscalYear" },
      { field: "VendorName" },
      { field: "InvoiceNumber" },
      { field: "Amount", filter: "agNumberColumnFilter" },
      { field: "CheckDate" },
      { field: "CheckNumber" },
      { field: "DateCashed" },
      { field: "VoucherStatus" },
      { field: "PostingStatus" },
    ],
    []
  );

  const defaultColDef = useMemo(() => {
    return {
      filter: "agTextColumnFilter",
      floatingFilter: true,
    };
  }, []);

  function onBtnExport() {
    const gridApi = gridRef.current?.api;
    if (gridApi) {
      gridApi.exportDataAsCsv();
    }
  }

  return (
    <div className="mt-48">
      <div className="flex flex-row justify-end my-4 space-x-4">
        <button
          onClick={onBtnExport}
          className="text-lg text-ch-cyan shadow-md w-fit p-2 rounded-md hover:shadow-lg hover:text-ch-cyan-dark"
        >
          <BsDownload />
        </button>
        <button
          onClick={fetchVendors}
          className="text-lg text-ch-cyan shadow-md w-fit p-2 rounded-md hover:shadow-lg hover:text-ch-cyan-dark"
        >
          <BsArrowClockwise />
        </button>
      </div>

      <div className="ag-theme-quartz" style={{ height: 500 }}>
        {/* Conditionally render the LoadingOverlay */}
        {loading && <LoadingOverlay />}
        <AgGridReact
          ref={gridRef}
          rowData={vendors}
          columnDefs={columnDefs}
          defaultColDef={defaultColDef}
          pagination={true}
          paginationPageSize={10}
          paginationPageSizeSelector={[10, 25, 50]}
        />
      </div>
    </div>
  );
}
