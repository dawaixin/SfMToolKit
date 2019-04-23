#include "pointmatcher/PointMatcher.h"
#include <cassert>
#include "boost/filesystem.hpp"
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>
#include <iostream>
#include <fstream>
#include <string>

using namespace std;

void validateArgs(int argc, char *argv[]);

int main(int argc, char *argv[]) {

    validateArgs(argc, argv);

    typedef PointMatcher<float> PM;
    typedef PM::DataPoints DP;

    //read the configuration file
    std::ifstream infile(argv[1]);

    //initialise a map to hold the parameters
    map<string, string> parameters;

    //read the configuration file and build the map
    std::string str;
    std::string key;
    std::string value;
    while (std::getline(infile, str)) {
        key = boost::algorithm::trim_copy(str.substr(0, str.find(':')));
        value = boost::algorithm::trim_copy(str.substr(str.find(':')+1, 1000));
        parameters.insert(pair<string, string>(key, value));
    }


    // Load point clouds
    const DP ref(DP::load(parameters["reference file"]));
    const DP data(DP::load(parameters["reading file"]));

    // Create the default ICP algorithm
    PM::ICP icp;
    PointMatcherSupport::Parametrizable::Parameters params;
    std::string name;

    // console outputs
    setLogger(PM::get().LoggerRegistrar.create("FileLogger"));

    // Prepare reading filters
    name = "MinDistDataPointsFilter";
    params["minDist"] = parameters["MinDistDataPointsFilter1"];
    std::shared_ptr<PM::DataPointsFilter> minDist_read = PM::get().DataPointsFilterRegistrar.create(name, params);
    params.clear();

    name = "RandomSamplingDataPointsFilter";
    params["prob"] = parameters["RandomSamplingDataPointsFilter1"];
    std::shared_ptr<PM::DataPointsFilter> rand_read = PM::get().DataPointsFilterRegistrar.create(name, params);
    params.clear();

    // Prepare reference filters
    name = "MinDistDataPointsFilter";
    params["minDist"] = parameters["MinDistDataPointsFilter2"];
    std::shared_ptr<PM::DataPointsFilter> minDist_ref = PM::get().DataPointsFilterRegistrar.create(name, params);
    params.clear();

    name = "RandomSamplingDataPointsFilter";
    params["prob"] = parameters["RandomSamplingDataPointsFilter2"];
    std::shared_ptr<PM::DataPointsFilter> rand_ref = PM::get().DataPointsFilterRegistrar.create(name, params);
    params.clear();

    // Prepare matching function
    name = "KDTreeMatcher";
    params["knn"] = parameters["KDTreeMatcher knn"];
    params["epsilon"] = parameters["KDTreeMatcher epsilon"];
    std::shared_ptr<PM::Matcher> kdtree = PM::get().MatcherRegistrar.create(name, params);
    params.clear();

    // Prepare outlier filters
    name = "TrimmedDistOutlierFilter";
    params["ratio"] = parameters["TrimmedDistOutlierFilter"];
    std::shared_ptr<PM::OutlierFilter> trim = PM::get().OutlierFilterRegistrar.create(name, params);
    params.clear();

    // Prepare error minimization
    name = "PointToPointErrorMinimizer";
    std::shared_ptr<PM::ErrorMinimizer> pointToPoint = PM::get().ErrorMinimizerRegistrar.create(name);

    // Prepare transformation checker filters
    name = "CounterTransformationChecker";
    params["maxIterationCount"] = parameters["CounterTransformationChecker"];
    std::shared_ptr<PM::TransformationChecker> maxIter = PM::get().TransformationCheckerRegistrar.create(name, params);
    params.clear();

    name = "DifferentialTransformationChecker";
    params["minDiffRotErr"] = parameters["DifferentialTransformationChecker minDiffRotErr"];
    params["minDiffTransErr"] = parameters["DifferentialTransformationChecker minDiffTransErr"];
    params["smoothLength"] = parameters["DifferentialTransformationChecker smoothLength"];
    std::shared_ptr<PM::TransformationChecker> diff = PM::get().TransformationCheckerRegistrar.create(name, params);
    params.clear();

    // Prepare inspector
    std::shared_ptr<PM::Inspector> nullInspect = PM::get().InspectorRegistrar.create("NullInspector");
    params.clear();

    // Prepare transformation
    std::shared_ptr<PM::Transformation> rigidTrans = PM::get().TransformationRegistrar.create("RigidTransformation");

    // Build ICP solution
    icp.readingDataPointsFilters.push_back(minDist_read);
    icp.readingDataPointsFilters.push_back(rand_read);

    icp.referenceDataPointsFilters.push_back(minDist_ref);
    icp.referenceDataPointsFilters.push_back(rand_ref);

    icp.matcher = kdtree;

    icp.outlierFilters.push_back(trim);

    icp.errorMinimizer = pointToPoint;

    icp.transformationCheckers.push_back(maxIter);
    icp.transformationCheckers.push_back(diff);

    // toggle to write vtk files per iteration
    icp.inspector = nullInspect;

    icp.transformations.push_back(rigidTrans);

    // Compute the transformation to express data in ref
    PM::TransformationParameters T = icp(data, ref);

    // Transform data to express it in ref
    DP data_out(data);
    icp.transformations.apply(data_out, T);

    // Safe files to see the results
    ref.save(parameters["working directory"] + "reference.vtk");
    data.save(parameters["working directory"] + "reading_in.vtk");
    data_out.save(parameters["working directory"] + "reading_out.vtk");
    string PLYexport = parameters["savePLY"];

    if (PLYexport == "1" ) {
        ref.save(parameters["working directory"] + "reference.ply");
        data.save(parameters["working directory"] + "reading_in.ply");
        data_out.save(parameters["working directory"] + "reading_out.ply");
    }

    std::cout << endl << "Final transformation:" << endl << T << endl;


    return 0;
}

void validateArgs(int argc, char *argv[])
{
    if (argc != 2)
    {
        cerr << "Wrong number of arguments, usage " << argv[0] << " icp-config.txt" << endl;
        cerr << "Will create 3 vtk files for inspection in the working directory specified in the configuration : reference.vtk, reading_in.vtk and reading_out.vtk" << endl;
        exit(1);
    }
}