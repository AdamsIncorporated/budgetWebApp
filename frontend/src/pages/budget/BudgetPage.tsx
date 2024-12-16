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
  Account: string;
  Actual: number;
  Variance: number;
  ForecastedAmount: number;
  ProposedBudget: number;
  BusinessCaseName: string;
  BusinessCaseAmount: number;
  Comments: string;
  TotalBudget: number;
}

export default function BudgetPage() {
  const [budgets, setBudgets] = useState<Vendor[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const gridRef = useRef<AgGridReact | null>(null);

  useEffect(() => {
    fetchVendors();
  }, []);

  const fetchVendors = async () => {
    setLoading(true);
    try {
      const response = await fetch("/api/budget/entry");
      if (!response.ok) {
        throw new Error("Failed to fetch vendor data");
      }
      const data = await response.json();
      setBudgets(data);
    } catch (error) {
      console.error("Error fetching vendor data:", error);
    } finally {
      setLoading(false);
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

  function onBtnExport() {
    const gridApi = gridRef.current?.api;
    if (gridApi) {
      gridApi.exportDataAsCsv();
    }
  }

  return (
    <div className="p-24">
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
        {loading && <LoadingOverlay />}
        <AgGridReact
          ref={gridRef}
          rowData={budgets}
          columnDefs={columnDefs}
          pagination={false}
        />
      </div>
    </div>
  );
}
