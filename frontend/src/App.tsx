import React, { useState } from "react";
import Plot from "react-plotly.js";
import "./App.css";
import { message, Form, Button, Row } from "antd";
import { Formik } from "formik";
import { FormItem, DatePicker, Select } from "formik-antd";
import { Typography } from "antd";

const { Title, Text } = Typography;

// interface DataPoint {
//   datelabel: Date | number | string;
//   value: number | string;
// }

// type DataPoints = DataPoint[];

const App = () => {
  const [result, setResult] = useState(new Date());

  const makeRequest = (
    startTime: Date,
    endTime: Date,
    productionTime: number
  ) => {
    const resquestObj = {
      earliest_start_time: startTime,
      deadline: endTime,
      prod_time_in_min: productionTime
    };
    console.log(resquestObj);
    const data = fetch("localhost:5000/schedule", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(resquestObj)
    })
      .then(response => response.json())
      .then(response => setResult(response))
      .catch(err => console.error(err));
  };

  return (
    <div
      className="App"
      style={{
        textAlign: "center",
        height: "100vh",
        display: "flex",
        alignItems: "center"
      }}
    >
      <Row style={{ margin: "0 auto" }}>
        <Title>Zero Emissions Factory</Title>
        <Text>
          A scheduler to optimize production lines with local green energy
          prodviders
        </Text>
        {
          <Formik
            initialValues={{
              startTime: new Date(),
              endTime: new Date(),
              productionTime: 0 //minutes
            }}
            onSubmit={async (values: any, actions: any) => {
              actions.setSubmitting(true);
              if (values) {
                const { startTime, endTime, productionTime } = values;
                await makeRequest(startTime, endTime, productionTime);
                actions.setSubmitting(false);
              }
              // message.error("Missing form data front end");
              // actions.setSubmitting(false);
            }}
            render={({ handleSubmit, isSubmitting, isValid }) => (
              <Form onSubmit={handleSubmit}>
                <FormItem name="startTime" label="Start Time">
                  <DatePicker
                    showTime
                    name="startTime"
                    style={{ width: 200 }}
                    format="YYYY-MM-DD HH:mm"
                  />
                </FormItem>
                <FormItem name="endTime" label="End Time">
                  <DatePicker
                    showTime
                    name="endTime"
                    style={{ width: 200 }}
                    format="YYYY-MM-DD HH:mm"
                  />
                </FormItem>
                <FormItem
                  name="productionTime"
                  label="Approximate Production Time"
                >
                  <Select name="productionTime" style={{ width: 200 }}>
                    {Select.renderOptions(
                      [15, 30, 45, 60].map(duration => ({
                        value: duration,
                        label: <span>{duration.toString() + " minutes"}</span>
                      }))
                    )}
                  </Select>
                </FormItem>
                <Form.Item>
                  <Button
                    icon="check"
                    type="primary"
                    style={{ background: "#1DA57A", border: "#1DA57A" }}
                    loading={isSubmitting}
                    disabled={!isValid}
                    onClick={() => {
                      handleSubmit();
                    }}
                  >
                    Optimize production
                  </Button>
                </Form.Item>
              </Form>
            )}
          />

          // <Plot
          //   data={[
          //     {
          //       x: result.payload.map(label => label),
          //       y: result.payload.map((_, value) => value),
          //       type: "bar",
          //       marker: { color: "green" }
          //     },
          //     { type: "bar", x: [1, 2, 3], y: [2, 5, 3] }
          //   ]}
          //   layout={{
          //     width: 450,
          //     height: 450,
          //     title: "Percentage of green energy"
          //   }}
          // />
        }
        <div>
          {Object.keys(result).map(key => (
            <div>{key}</div>
          ))}
        </div>
      </Row>
    </div>
  );
};

export default App;
